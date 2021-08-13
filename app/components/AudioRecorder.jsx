import React, { useState, useRef } from "react";
import AudioReactRecorder, { RecordState } from "audio-react-recorder";
import axios from "axios";

const AudioRecorder = () => {
  const wrapperRef = useRef();
  const audioRef = useRef();
  const [record, setRecord] = useState(false);

  const onStop = (recordedBlob) => {
    console.log(recordedBlob);

    const fd = new FormData();
    fd.append("file", recordedBlob.blob);

    axios
      .post("http://41352fc471fa.ngrok.io/vsigverify", fd, {
        headers: {
          "Content-Type": "multipart/form-data",
          enctype: "multipart/form-data",
        },
      })
      .then(async (res) => {
        console.log(res.data);
      });
  };

  if (typeof window === "undefined" || !process.browser) return null;

  return (
    <div ref={wrapperRef}>
      <h1 className='text-left text-3xl text-blue-800 font-bold mb-4'>
        Voice Signature
      </h1>
      <AudioReactRecorder
        ref={audioRef}
        state={record}
        backgroundColor='rgb(79, 70, 229)'
        foregroundColor='rgb(255,255,255)'
        canvasHeight={50}
        onStop={onStop}
      />
      {record === RecordState.START ? (
        <button
          className='mt-4 inline-flex rounded-full bg-indigo-600 hover:bg-indigo-700 focus:outline-none text-white font-bold px-6 py-2 focus:ring ring-indigo-600 ring-offset-2'
          onClick={() => setRecord(RecordState.STOP)}
          type='button'>
          Stop Recording
        </button>
      ) : (
        <button
          className='mt-4 inline-flex rounded-full bg-indigo-600 hover:bg-indigo-700 focus:outline-none text-white font-bold px-6 py-2 focus:ring ring-indigo-600 ring-offset-2'
          onClick={() => setRecord(RecordState.START)}
          type='button'>
          Start Recording
        </button>
      )}
    </div>
  );
};

export default AudioRecorder;
