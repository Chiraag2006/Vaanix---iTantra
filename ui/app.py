import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from semantic.encoder import encode_message
from communication.semantic_transport import transmit_semantic_packet
from integration.pipeline import semantic_decode
from tts.tts_engine import text_to_speech


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

st.caption(
    "Meaning is transmitted instead of the original speech waveform."
)

st.divider()


# --------------------------------------------------
# INPUT
# --------------------------------------------------

st.header("🎤 Voice / Message Input")

original_text = st.text_input(
    "Enter message to transmit",
    value="Send medical supplies to sector four immediately."
)

st.info(
    f"Input message: {original_text}"
)


# --------------------------------------------------
# SEMANTIC ENCODING
# --------------------------------------------------

packet = encode_message(original_text)


# --------------------------------------------------
# SEMANTIC REPRESENTATION
# --------------------------------------------------

st.header("🧠 Semantic Representation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Intent", packet.intent)

with col2:
    st.metric("Object", packet.object)

with col3:
    st.metric(
        "Location",
        packet.location.replace("_", " ")
    )

with col4:
    st.metric("Priority", packet.priority)


# --------------------------------------------------
# COMMUNICATION CHANNEL
# --------------------------------------------------

st.header("📡 Communication Channel")

st.metric(
    "BPSK SNR",
    "5 dB"
)

st.info(
    "Current BPSK radio simulation uses a fixed 5 dB SNR."
)


# --------------------------------------------------
# TRANSMISSION
# --------------------------------------------------

st.divider()

if st.button(
    "🚀 Transmit Semantic Message",
    use_container_width=True
):

    start_time = time.perf_counter()

    result = transmit_semantic_packet(
        packet
    )

    end_time = time.perf_counter()

    latency_ms = (
        end_time - start_time
    ) * 1000

    st.session_state["demo_run"] = True
    st.session_state["result"] = result
    st.session_state["latency_ms"] = latency_ms

    if result["success"]:

        recovered_packet = result["packet"]

        recovered_text = semantic_decode(
            recovered_packet
        )

        st.session_state[
            "recovered_text"
        ] = recovered_text

        audio_file = text_to_speech(
            recovered_text
        )

        st.session_state[
            "audio_file"
        ] = str(audio_file)

    else:

        st.session_state[
            "recovered_text"
        ] = ""

        st.session_state[
            "audio_file"
        ] = ""


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

st.divider()

st.header("🔄 Communication Pipeline")

pipeline_steps = [
    "🎤 Input",
    "🧠 Semantic Encoding",
    "📦 Packetisation",
    "🛡️ CRC",
    "🧬 Hamming FEC",
    "🔀 Interleaving",
    "📡 BPSK + AWGN",
    "🔀 Deinterleaving",
    "🧬 FEC Decode",
    "✅ CRC Check",
    "🔊 Neural TTS"
]

st.write(
    " → ".join(pipeline_steps)
)


# --------------------------------------------------
# RECEIVER
# --------------------------------------------------

if st.session_state.get(
    "demo_run",
    False
):

    result = st.session_state[
        "result"
    ]

    st.divider()

    st.header("📥 Receiver")

    if result["success"]:

        st.success(
            "✅ Semantic packet successfully recovered"
        )

        # ------------------------------------------
        # STATUS
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("CRC VALID")

        with col2:
            st.success("HAMMING FEC RECOVERED")

        with col3:
            st.success("BPSK LINK OK")

        # ------------------------------------------
        # RECOVERED MESSAGE
        # ------------------------------------------

        recovered_text = st.session_state.get(
            "recovered_text",
            ""
        )

        st.subheader(
            "Recovered Message"
        )

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

        if (
            audio_file
            and Path(audio_file).exists()
        ):

            st.subheader(
                "🔊 Reconstructed Speech"
            )

            st.audio(
                audio_file,
                format="audio/mp3"
            )

        # ------------------------------------------
        # METRICS
        # ------------------------------------------

        st.subheader(
            "📊 Transmission Metrics"
        )

        latency_ms = st.session_state.get(
            "latency_ms",
            0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Semantic Payload",
                f'{result["payload_size"]} bytes'
            )

        with col2:

            st.metric(
                "Packet + CRC",
                f'{result["packet_size"]} bytes'
            )

        with col3:

            st.metric(
                "Transmitted Bits",
                result["tx_bits"]
            )

        with col4:

            st.metric(
                "Processing Time",
                f"{latency_ms:.2f} ms"
            )

        # ------------------------------------------
        # CRC
        # ------------------------------------------

        st.subheader(
            "🔐 CRC Verification"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f'**Received CRC:** '
                f'{result["received_crc"]}'
            )

        with col2:

            st.write(
                f'**Calculated CRC:** '
                f'{result["calculated_crc"]}'
            )

        # ------------------------------------------
        # RADIO
        # ------------------------------------------

        st.subheader(
            "📡 Radio Details"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "FEC Bits",
                result["fec_bits"]
            )

        with col2:

            st.metric(
                "TX Bits",
                result["tx_bits"]
            )

        with col3:

            st.metric(
                "Modulation",
                "BPSK"
            )

    else:

        st.error(
            "❌ Transmission failed."
        )

        st.warning(
            "CRC validation failed at the receiver."
        )