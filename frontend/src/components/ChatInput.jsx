import {
  Plus,
  Mic,
  ArrowUp,
  Square
} from "lucide-react";

import { useState, useRef, useEffect } from "react";

function ChatInput({ onSubmit, disabled, onVoiceSubmit, onImageSubmit,mode="data"}) {

  const [query, setQuery] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);
  const timerIntervalRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const handlePaste = (e) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        if (items[i].type.startsWith('image/')) {
          e.preventDefault();
          const file = items[i].getAsFile();
          if (file && onImageSubmit) {
            onImageSubmit(file);
          }
          break;
        }
      }
    };

    document.addEventListener('paste', handlePaste);
    return () => {
      document.removeEventListener('paste', handlePaste);
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [onImageSubmit]);

  const startRecording = async () => {
      try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true});

      const track = stream.getAudioTracks()[0];

      console.log("Recording from:", track.label);

      console.log(track.getSettings());
      
      streamRef.current = stream;
      audioChunksRef.current = [];

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });

        stream.getTracks().forEach(track => track.stop());
        streamRef.current = null;

        onVoiceSubmit(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      timerIntervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    }catch (error) {
      console.error(error);
      console.error("name:", error.name);
      console.error("message:", error.message);

      alert(
        `Mic Error: ${error.name}\n${error.message}`
      );
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const send = () => {
    if (!query.trim() || disabled) return;
    onSubmit(query, false);
    setQuery("");
  };

  const handleImageClick = () => {
    fileInputRef.current?.click();
  };

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    if (onImageSubmit) {
      onImageSubmit(file);
    }

    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="
      border-t
      border-sky-100
      bg-white
      p-4
    ">

      <div className="
        max-w-4xl
        mx-auto
      ">

        {isRecording && (
          <div className="
            mb-4
            flex
            items-center
            gap-3
            px-4
            py-3
            bg-red-50
            border
            border-red-200
            rounded-2xl
          ">
            <div className="
              w-3
              h-3
              bg-red-500
              rounded-full
              animate-pulse
            "></div>
            <span className="text-sm text-red-600 font-medium">
              Recording: {formatTime(recordingTime)}
            </span>
          </div>
        )}

        <div className={`
          rounded-3xl
          border
          border-sky-200
          px-5
          py-2.5
          flex
          items-center
          gap-4
          shadow-sm
          ${disabled || isRecording ? 'opacity-50 cursor-not-allowed' : ''}
        `}>

          <button
            onClick={handleImageClick}
            disabled={disabled || isRecording}
            className="text-sky-500 hover:cursor-pointer disabled:cursor-not-allowed"
            title="Attach photo"
          >
            <Plus size={20} />
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="hidden"
            disabled={disabled || isRecording}
          />

          <input
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            onKeyDown={(e) =>
              e.key === "Enter" && !disabled && !isRecording && send()
            }
            placeholder={mode === "knowledge" ? "Ask about health protocols..." : "Ask about your village data..."}
            disabled={disabled || isRecording}
            className="
              flex-1
              outline-none
              disabled:bg-gray-50
            "
          />

          <button
            onClick={toggleRecording}
            disabled={disabled}
            className={`
              p-1
              hover:cursor-pointer
              transition-colors
              ${isRecording
                ? 'text-red-500'
                : 'text-sky-500'
              }
            `}
            title={isRecording ? "Stop recording" : "Start recording"}
          >
            {isRecording ? (
              <Square size={20} />
            ) : (
              <Mic size={20} />
            )}
          </button>

          <button
            onClick={send}
            disabled={disabled || isRecording}
            className="
              h-9
              w-9
              rounded-full
              bg-sky-500
              text-white
              px-2
              disabled:opacity-50
              disabled:cursor-not-allowed
              hover:cursor-pointer
            "
          >
            <ArrowUp size={19} />
          </button>

        </div>

      </div>

    </div>
  );
}

export default ChatInput;