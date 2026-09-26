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


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="TANTRA",
    page_icon="📡",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("📡 TANTRA")
st.subheader("Semantic Voice Communication System")

st.caption(
    "Meaning is transmitted instead of the original speech waveform."
)

st.divider()


# ==================================================
# INPUT
# ==================================================

st.header("🎤 Voice / Message Input")

original_text = st.text_input(
    "Enter message to transmit",
    value="Send medical supplies to sector four immediately."
)

st.info(
    f"Input message: {original_text}"
)


# ==================================================
# SEMANTIC ENCODING
# ==================================================

packet = encode_message(original_text)


# ==================================================
# SEMANTIC REPRESENTATION
# ==================================================

st.header("🧠 Semantic Representation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Intent",
        packet.intent
    )

with col2:
    st.metric(
        "Object",
        packet.object
    )

with col3:
    st.metric(
        "Location",
        packet.location.replace("_", " ")
    )

with col4:
    st.metric(
        "Priority",
        packet.priority
    )


# ==================================================
# COMMUNICATION CHANNEL
# ==================================================

st.header("📡 Communication Channel")

snr_db = st.slider(
    "BPSK Channel SNR (dB)",
    min_value=0,
    max_value=15,
    value=8,
    step=1
)

st.caption(
    "Lower SNR increases channel errors. "
    "Higher SNR improves reliable semantic recovery."
)


# ==================================================
# TRANSMISSION BUTTON
# ==================================================

st.divider()

if st.button(
    "🚀 Transmit Semantic Message",
    use_container_width=True
):

    start_time = time.perf_counter()

    result = transmit_semantic_packet(
        packet,
        snr_db=snr_db
    )

    end_time = time.perf_counter()

    processing_time_ms = (
        end_time - start_time
    ) * 1000

    st.session_state["demo_run"] = True
    st.session_state["result"] = result
    st.session_state["processing_time_ms"] = (
        processing_time_ms
    )

    if result["success"]:

        recovered_packet = result["packet"]

        recovered_text = semantic_decode(
            recovered_packet
        )

        st.session_state["recovered_text"] = (
            recovered_text
        )

        audio_file = text_to_speech(
            recovered_text
        )

        st.session_state["audio_file"] = (
            str(audio_file)
        )

    else:

        st.session_state["recovered_text"] = ""
        st.session_state["audio_file"] = ""


# ==================================================
# COMMUNICATION PIPELINE
# ==================================================

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


# ==================================================
# RECEIVER
# ==================================================

if st.session_state.get(
    "demo_run",
    False
):

    result = st.session_state["result"]

    st.divider()

    st.header("📥 Receiver")


    # ==================================================
    # SUCCESS
    # ==================================================

    if result["success"]:

        st.success(
            "✅ Semantic packet successfully recovered"
        )

        # ----------------------------------------------
        # STATUS
        # ----------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("CRC VALID")

        with col2:
            st.success("HAMMING FEC RECOVERED")

        with col3:
            st.success("BPSK LINK OK")


        # ----------------------------------------------
        # RECOVERED MESSAGE
        # ----------------------------------------------

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


        # ----------------------------------------------
        # RECONSTRUCTED SPEECH
        # ----------------------------------------------

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


        # ==================================================
        # CHANNEL METRICS
        # ==================================================

        st.subheader(
            "📊 Communication Metrics"
        )

        processing_time_ms = (
            st.session_state.get(
                "processing_time_ms",
                0
            )
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "SNR",
                f'{result["snr_db"]} dB'
            )

        with col2:
            st.metric(
                "Raw BER",
                f'{result["ber"] * 100:.2f}%'
            )

        with col3:
            st.metric(
                "Semantic Payload",
                f'{result["payload_size"]} bytes'
            )

        with col4:
            st.metric(
                "Processing Time",
                f"{processing_time_ms:.2f} ms"
            )


        # ==================================================
        # PACKET / BIT METRICS
        # ==================================================

        st.subheader(
            "📦 Packet & FEC Details"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Packet + CRC",
                f'{result["packet_size"]} bytes'
            )

        with col2:
            st.metric(
                "FEC Bits",
                result["fec_bits"]
            )

        with col3:
            st.metric(
                "TX Bits",
                result["tx_bits"]
            )

        with col4:
            st.metric(
                "RX Bits",
                result["rx_bits"]
            )


        # ==================================================
        # CRC VERIFICATION
        # ==================================================

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


        # ==================================================
        # SEMANTIC PACKET
        # ==================================================

        st.subheader(
            "🧠 Recovered Semantic Packet"
        )

        recovered_packet = result["packet"]

        st.json({
            "version": recovered_packet.version,
            "language": recovered_packet.language,
            "intent": recovered_packet.intent,
            "object": recovered_packet.object,
            "location": recovered_packet.location,
            "priority": recovered_packet.priority
        })


    # ==================================================
    # FAILURE
    # ==================================================

    else:

        st.error(
            "❌ Semantic packet could not be recovered."
        )

        st.warning(
            "The noisy channel produced enough errors "
            "that Hamming FEC could not completely recover "
            "the packet, so CRC rejected it."
        )


        # ----------------------------------------------
        # FAILURE METRICS
        # ----------------------------------------------

        st.subheader(
            "📊 Failed Transmission Metrics"
        )

        processing_time_ms = (
            st.session_state.get(
                "processing_time_ms",
                0
            )
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "SNR",
                f'{result["snr_db"]} dB'
            )

        with col2:
            st.metric(
                "Raw BER",
                f'{result["ber"] * 100:.2f}%'
            )

        with col3:
            st.metric(
                "Packet Size",
                f'{result["packet_size"]} bytes'
            )

        with col4:
            st.metric(
                "Processing Time",
                f"{processing_time_ms:.2f} ms"
            )


        # ----------------------------------------------
        # CRC DETAILS
        # ----------------------------------------------

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


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "iTantra • VaaniX • Semantic communication prototype"
)