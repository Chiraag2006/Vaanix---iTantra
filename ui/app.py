import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from speech.stt_engine import speech_to_text
from semantic.encoder import encode_message
from communication.semantic_transport import transmit_semantic_packet
from integration.pipeline import semantic_decode
from tts.tts_engine import text_to_speech


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TANTRA",
    page_icon="📡",
    layout="wide"
)

st.title("📡 TANTRA")
st.subheader("Semantic Voice Communication System")
st.caption(
    "Meaning is transmitted instead of the original speech waveform."
)

st.divider()


# =========================================================
# SESSION STATE
# =========================================================

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "language_code" not in st.session_state:
    st.session_state.language_code = None

if "language_name" not in st.session_state:
    st.session_state.language_name = None

if "language_probability" not in st.session_state:
    st.session_state.language_probability = 0.0

if "packet" not in st.session_state:
    st.session_state.packet = None

if "stt_done" not in st.session_state:
    st.session_state.stt_done = False

if "transmission_result" not in st.session_state:
    st.session_state.transmission_result = None

if "recovered_text" not in st.session_state:
    st.session_state.recovered_text = None

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

if "processing_time" not in st.session_state:
    st.session_state.processing_time = None


# =========================================================
# VOICE INPUT
# =========================================================

st.header("🎤 Voice Input")

st.write(
    "Press the microphone button, speak your message, "
    "then stop recording."
)

recorded_audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav",
    key="voice_recorder",
)


# =========================================================
# SAVE NEW RECORDING TO SESSION STATE
# =========================================================

if recorded_audio is not None:

    new_audio = recorded_audio["bytes"]

    # Only process when a new recording is received.
    if new_audio != st.session_state.audio_bytes:

        st.session_state.audio_bytes = new_audio

        # Reset results belonging to the previous recording.
        st.session_state.transcript = ""
        st.session_state.language_code = None
        st.session_state.language_name = None
        st.session_state.language_probability = 0.0
        st.session_state.packet = None
        st.session_state.stt_done = False
        st.session_state.transmission_result = None
        st.session_state.recovered_text = None
        st.session_state.audio_file = None
        st.session_state.processing_time = None

        # Save microphone recording.
        input_audio = PROJECT_ROOT / "input_voice.wav"

        with open(input_audio, "wb") as f:
            f.write(new_audio)

        # -------------------------------------------------
        # STT
        # -------------------------------------------------

        with st.spinner("🎧 Converting speech to text..."):

            stt_result = speech_to_text(str(input_audio))

        transcript = stt_result["text"]
        detected_language = stt_result["language"]

        if detected_language.startswith("hi"):
            language_code = "hi"
            language_name = "Hindi"
        else:
            language_code = "en"
            language_name = "English"

        st.session_state.transcript = transcript
        st.session_state.language_code = language_code
        st.session_state.language_name = language_name
        st.session_state.language_probability = (
            stt_result["language_probability"]
        )
        st.session_state.stt_done = True

        # -------------------------------------------------
        # SEMANTIC ENCODING
        # -------------------------------------------------

        packet = encode_message(transcript)
        packet.language = language_code

        st.session_state.packet = packet


# =========================================================
# SHOW STT RESULT
# =========================================================

if st.session_state.stt_done:

    st.subheader("📝 Speech Recognition")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Detected Language",
            st.session_state.language_name
        )

    with col2:
        st.metric(
            "Language Confidence",
            f"{st.session_state.language_probability * 100:.1f}%"
        )

    st.info(
        f"**Transcript:** {st.session_state.transcript}"
    )


# =========================================================
# SHOW SEMANTIC PACKET
# =========================================================

if st.session_state.packet is not None:

    packet = st.session_state.packet

    st.subheader("🧠 Semantic Compression")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Intent", packet.intent)

    with col2:
        st.metric("Object", packet.object)

    with col3:
        st.metric("Location", packet.location)

    with col4:
        st.metric("Priority", packet.priority)


    # =====================================================
    # CHANNEL SETTINGS
    # =====================================================

    st.subheader("📡 Communication Channel")

    snr_db = st.slider(
        "Channel SNR (dB)",
        min_value=0,
        max_value=15,
        value=10,
        step=1
    )

    st.caption(
        "Lower SNR represents a noisier communication channel."
    )


    # =====================================================
    # TRANSMIT
    # =====================================================

    if st.button(
        "🚀 Transmit Voice Message",
        use_container_width=True
    ):

        start_time = time.perf_counter()

        with st.spinner(
            "📡 Transmitting semantic packet..."
        ):

            result = transmit_semantic_packet(
                packet,
                snr_db=snr_db
            )

        processing_time = time.perf_counter() - start_time

        # Store result so it survives Streamlit reruns.
        st.session_state.transmission_result = result
        st.session_state.processing_time = processing_time

        # Clear old reconstructed output.
        st.session_state.recovered_text = None
        st.session_state.audio_file = None

        if result["success"]:

            recovered_packet = result["packet"]

            recovered_text = semantic_decode(
                recovered_packet
            )

            st.session_state.recovered_text = recovered_text

            with st.spinner(
                "🔊 Generating reconstructed speech..."
            ):

                audio_file = text_to_speech(
                    recovered_text,
                    language=recovered_packet.language
                )

            st.session_state.audio_file = audio_file

        st.rerun()


# =========================================================
# SHOW TRANSMISSION RESULTS
# =========================================================

if st.session_state.transmission_result is not None:

    result = st.session_state.transmission_result

    st.subheader("📊 Transmission Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "BER",
            f"{result['ber'] * 100:.2f}%"
        )

    with col2:
        st.metric(
            "CRC",
            "VALID"
            if result["crc_valid"]
            else "INVALID"
        )

    with col3:
        st.metric(
            "Packet Size",
            f"{result['packet_size']} bytes"
        )

    with col4:
        st.metric(
            "Processing Time",
            f"{st.session_state.processing_time:.2f} s"
        )


    # =====================================================
    # FAILED TRANSMISSION
    # =====================================================

    if not result["success"]:

        st.error(
            "❌ Packet could not be recovered. "
            "CRC rejected the corrupted packet."
        )

        st.warning(
            "Try increasing the SNR and transmit again."
        )


    # =====================================================
    # SUCCESSFUL TRANSMISSION
    # =====================================================

    else:

        recovered_packet = result["packet"]

        st.success(
            "✅ Packet successfully recovered."
        )


        # -------------------------------------------------
        # RECOVERED PACKET
        # -------------------------------------------------

        st.subheader("📦 Recovered Semantic Packet")

        st.json({
            "version": recovered_packet.version,
            "language": recovered_packet.language,
            "intent": recovered_packet.intent,
            "object": recovered_packet.object,
            "location": recovered_packet.location,
            "priority": recovered_packet.priority,
        })


        # -------------------------------------------------
        # RECONSTRUCTED MESSAGE
        # -------------------------------------------------

        st.subheader("🔊 Reconstructed Message")

        st.info(
            st.session_state.recovered_text
        )


        # -------------------------------------------------
        # AUDIO
        # -------------------------------------------------

        if st.session_state.audio_file is not None:

            st.audio(
                str(st.session_state.audio_file),
                format="audio/mp3"
            )


        # -------------------------------------------------
        # TRANSPORT DETAILS
        # -------------------------------------------------

        st.subheader("📡 Transport Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"**SNR:** {result['snr_db']} dB"
            )

            st.write(
                f"**BER:** {result['ber'] * 100:.2f}%"
            )

        with col2:

            st.write(
                f"**Payload:** "
                f"{result['payload_size']} bytes"
            )

            st.write(
                f"**Packet + CRC:** "
                f"{result['packet_size']} bytes"
            )

        with col3:

            st.write(
                f"**FEC encoded bits:** "
                f"{result['fec_bits']}"
            )

            st.write(
                f"**Transmitted bits:** "
                f"{result['tx_bits']}"
            )


        # -------------------------------------------------
        # CRC DETAILS
        # -------------------------------------------------

        with st.expander("CRC Details"):

            st.write(
                f"Received CRC: "
                f"`{result['received_crc']}`"
            )

            st.write(
                f"Calculated CRC: "
                f"`{result['calculated_crc']}`"
            )

            st.write(
                "CRC verification: ✅ VALID"
            )


else:

    if not st.session_state.stt_done:

        st.info(
            "🎤 Record a voice message to begin."
        )