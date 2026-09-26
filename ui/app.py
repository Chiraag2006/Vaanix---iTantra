import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from semantic.packet_schema import SemanticPacket
from communication.channel_simulator import transmit
from integration.pipeline import semantic_decode
from tts.tts_engine import text_to_speech
from evaluation.metrics import (
    estimate_packet_size,
    measure_latency,
    semantic_fidelity
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TANTRA",
    page_icon="📡",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📡 TANTRA")
st.subheader("Semantic Voice Communication System")

st.divider()


# --------------------------------------------------
# INPUT
# --------------------------------------------------

st.header("🎤 Voice Input")

original_text = st.text_input(
    "Enter message to transmit",
    value="Send medical supplies to sector four immediately."
)

st.info(
    f"Input message: {original_text}"
)


# --------------------------------------------------
# SEMANTIC PACKET
# --------------------------------------------------

packet = SemanticPacket(
    version=1,
    language="en",
    intent="SUPPLY_REQUEST",
    object="MEDICINE",
    location="SECTOR_4",
    priority="HIGH"
)


# --------------------------------------------------
# SEMANTIC REPRESENTATION
# --------------------------------------------------

st.header("🧠 Semantic Representation")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Intent", packet.intent)

with col2:
    st.metric("Object", packet.object)

with col3:
    st.metric("Priority", packet.priority)

st.write(
    f"**Location:** "
    f"{packet.location.replace('_', ' ')}"
)


# --------------------------------------------------
# PACKET SIZE
# --------------------------------------------------

packet_size = estimate_packet_size(packet)


# --------------------------------------------------
# TRANSMISSION
# --------------------------------------------------

st.divider()

st.header("📦 Transmission")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Original Audio",
        "Not measured"
    )

with col2:
    st.metric(
        "Semantic Packet",
        f"{packet_size} bytes"
    )

with col3:
    st.metric(
        "Packet Loss",
        "0%"
    )


# --------------------------------------------------
# CHANNEL SIMULATION
# --------------------------------------------------

st.header("📡 Channel Simulation")

packet_loss_percent = st.slider(
    "Packet Loss",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)

corruption_percent = st.slider(
    "Packet Corruption",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)

packet_loss = packet_loss_percent / 100
corruption_probability = corruption_percent / 100


# --------------------------------------------------
# PROTECTION
# --------------------------------------------------

st.subheader("🛡️ Communication Protection")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CRC", "ON")

with col2:
    st.metric("FEC Redundancy", "3×")

with col3:
    st.metric("Interleaving", "ON")


# --------------------------------------------------
# RUN DEMO
# --------------------------------------------------

if st.button("🚀 Run TANTRA Demo"):

    received_packet, crc_valid, fec_recovered = transmit(
        packet,
        packet_loss,
        corruption_probability
    )

    if received_packet is None:

        st.session_state["demo_run"] = True
        st.session_state["packet_lost"] = True
        st.session_state["crc_valid"] = False
        st.session_state["fec_recovered"] = False

    else:

        recovered_text, latency_ms = measure_latency(
            semantic_decode,
            received_packet
        )

        audio_file = text_to_speech(
            recovered_text
        )

        fidelity = semantic_fidelity(
            original_text,
            recovered_text
        )

        st.session_state["demo_run"] = True
        st.session_state["packet_lost"] = False
        st.session_state["crc_valid"] = crc_valid
        st.session_state["fec_recovered"] = fec_recovered
        st.session_state["recovered_text"] = recovered_text
        st.session_state["audio_file"] = str(audio_file)
        st.session_state["latency_ms"] = latency_ms
        st.session_state["fidelity"] = fidelity


# --------------------------------------------------
# PIPELINE STATUS
# --------------------------------------------------

st.divider()

st.header("🔄 TANTRA Pipeline")

pipeline_steps = [
    "🎤 Input",
    "🧠 Semantic Encoding",
    "🛡️ FEC + CRC",
    "📡 Channel",
    "📥 Recovery",
    "🔊 Neural TTS"
]

st.write(" → ".join(pipeline_steps))


# --------------------------------------------------
# RECEIVER
# --------------------------------------------------

st.divider()

st.header("📥 Receiver")

if st.session_state.get("demo_run", False):

    if st.session_state.get("packet_lost", False):

        st.error(
            "🔴 Packet could not be recovered."
        )

        st.warning(
            "All redundant copies were lost "
            "or failed CRC verification."
        )

    else:

        crc_valid = st.session_state.get(
            "crc_valid",
            False
        )

        fec_recovered = st.session_state.get(
            "fec_recovered",
            False
        )

        col1, col2 = st.columns(2)

        with col1:

            if crc_valid:
                st.success(
                    "🟢 CRC CHECK PASSED"
                )
            else:
                st.error(
                    "🔴 CRC CHECK FAILED"
                )

        with col2:

            if fec_recovered:
                st.success(
                    "🟢 FEC RECOVERY SUCCESS"
                )
            else:
                st.info(
                    "ℹ️ Direct packet received"
                )


        recovered_text = st.session_state.get(
            "recovered_text",
            ""
        )

        st.subheader("Recovered Message")

        st.success(
            recovered_text
        )


        # ------------------------------------------
        # AUDIO
        # ------------------------------------------

        audio_file = st.session_state.get(
            "audio_file",
            ""
        )

        st.write(
            "🔊 Reconstructed speech:"
        )

        if Path(audio_file).exists():

            st.audio(
                audio_file,
                format="audio/mp3"
            )

        else:

            st.error(
                f"Audio file was not found:\n"
                f"{audio_file}"
            )


        # ------------------------------------------
        # EVALUATION
        # ------------------------------------------

        st.subheader("📊 Evaluation")

        latency_ms = st.session_state.get(
            "latency_ms",
            0
        )

        fidelity = st.session_state.get(
            "fidelity",
            0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Packet Size",
                f"{packet_size} bytes"
            )

        with col2:
            st.metric(
                "Packet Loss",
                f"{packet_loss_percent}%"
            )

        with col3:
            st.metric(
                "Latency",
                f"{latency_ms:.2f} ms"
            )

        with col4:
            st.metric(
                "Semantic Fidelity",
                f"{fidelity * 100:.0f}%"
            )

else:

    st.info(
        "Enter a message and press "
        "'Run TANTRA Demo' to start."
    )