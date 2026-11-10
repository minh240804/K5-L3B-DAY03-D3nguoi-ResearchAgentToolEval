from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"
PROVIDERS = ("gemini", "openai", "openrouter", "anthropic", "ollama")


st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")


@st.cache_data(show_spinner=False)
def load_artifacts() -> tuple[str, list[dict[str, Any]]]:
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    declarations = load_tool_declarations(TOOLS_PATH)
    return system_prompt, to_openai_tools(declarations)


def create_transcript(provider_name: str, model: str | None, version: str) -> tuple[dict[str, Any], Path]:
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join(
        [safe_slug(version), safe_slug(provider_name), timestamp]
    )
    transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    transcript: dict[str, Any] = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(SYSTEM_PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": st.session_state.history_window,
        "max_tool_rounds": st.session_state.max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    return transcript, transcript_path


def reset_chat() -> None:
    for key in (
        "history",
        "turns",
        "transcript",
        "transcript_path",
        "awaiting_user",
    ):
        st.session_state.pop(key, None)


def initialize_state() -> None:
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("turns", [])
    st.session_state.setdefault("awaiting_user", False)


def render_tool_activity(turn: dict[str, Any]) -> None:
    rounds = turn.get("rounds", [])
    if not rounds:
        return

    call_count = sum(len(round_record.get("tool_calls", [])) for round_record in rounds)
    if call_count == 0:
        return

    with st.expander(f"Tool activity ({call_count} call{'s' if call_count != 1 else ''})"):
        for round_record in rounds:
            calls = round_record.get("tool_calls", [])
            results = round_record.get("tool_results", [])
            for index, call in enumerate(calls):
                st.markdown(f"**Round {round_record['round']} · `{call['name']}`**")
                st.caption("Arguments")
                st.json(call.get("args", {}), expanded=True)
                if index < len(results):
                    st.caption("Result")
                    st.json(results[index].get("result", {}), expanded=True)


def render_chat_history() -> None:
    for turn in st.session_state.turns:
        with st.chat_message("user"):
            st.markdown(turn["user"])
        with st.chat_message("assistant"):
            if turn.get("status") == "provider_error":
                st.error(turn.get("error", "Provider error"))
            else:
                st.markdown(turn.get("assistant_text") or "")
            render_tool_activity(turn)


initialize_state()

st.title("🔎 Research Agent")
st.caption("Chat với agent và quan sát các tool call/tool result trong từng lượt.")

conversation_started = bool(st.session_state.turns)
with st.sidebar:
    st.header("Cấu hình")
    provider_name = st.selectbox("Provider", PROVIDERS, disabled=conversation_started)
    model_input = st.text_input(
        "Model (tùy chọn)",
        placeholder="Dùng model mặc định của provider",
        disabled=conversation_started,
    )
    version = st.text_input("Artifact version", value="v0", disabled=conversation_started)
    st.number_input(
        "History window",
        min_value=1,
        max_value=50,
        value=5,
        key="history_window",
        disabled=conversation_started,
    )
    st.number_input(
        "Max tool rounds",
        min_value=1,
        max_value=20,
        value=4,
        key="max_tool_rounds",
        disabled=conversation_started,
    )
    st.caption("API key được đọc từ môi trường/.env và không được hiển thị trên UI.")
    if st.button("Cuộc trò chuyện mới", use_container_width=True):
        reset_chat()
        st.rerun()

render_chat_history()

if st.session_state.awaiting_user:
    st.info("Agent đang chờ thông tin bổ sung của bạn.")

prompt = st.chat_input(
    "Trả lời câu hỏi của agent..." if st.session_state.awaiting_user else "Nhập request của bạn..."
)

if prompt:
    system_prompt, openai_tools = load_artifacts()
    selected_model = model_input.strip() or None

    if "transcript" not in st.session_state:
        provider_for_metadata = make_provider(provider_name)
        resolved_model = selected_model or getattr(provider_for_metadata, "default_model", None)
        transcript, transcript_path = create_transcript(
            provider_name,
            resolved_model,
            version.strip() or "v0",
        )
        st.session_state.transcript = transcript
        st.session_state.transcript_path = transcript_path
    else:
        provider_for_metadata = make_provider(provider_name)

    turn_index = len(st.session_state.turns) + 1
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, int(st.session_state.history_window)),
        {"role": "user", "content": prompt},
    ]
    turn_record: dict[str, Any] = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Agent đang xử lý..."):
                result = run_model_tool_loop(
                    provider=provider_for_metadata,
                    messages=messages,
                    tools=openai_tools,
                    model=selected_model,
                    max_tool_rounds=int(st.session_state.max_tool_rounds),
                )
            turn_record.update(result)
            assistant_text = result["assistant_text"]
            st.markdown(assistant_text)
            render_tool_activity(turn_record)
            st.session_state.history.extend(
                [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": assistant_text},
                ]
            )
            st.session_state.awaiting_user = result["status"] == "waiting_for_user"
        except Exception as exc:
            turn_record.update(
                {
                    "status": "provider_error",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            st.error(turn_record["error"])
            st.session_state.awaiting_user = False

    turn_record["ended_at"] = now_iso()
    st.session_state.turns.append(turn_record)
    st.session_state.transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
    st.caption(f"Transcript: {st.session_state.transcript_path.name}")
