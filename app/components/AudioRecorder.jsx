import React, { useState, useRef } from "react";
import AudioReactRecorder, { RecordState } from "audio-react-recorder";
import { CheckCircleIcon, XCircleIcon } from "@heroicons/react/outline";
import axios from "axios";

const AudioRecorder = () => {
  const wrapperRef = useRef();
  const audioRef = useRef();
  const [record, setRecord] = useState(false);
  const [success, setSuccess] = useState(null);

  const onStop = (recordedBlob) => {
    console.log(recordedBlob);

    const fd = new FormData();
    fd.append("file", recordedBlob.blob);

    axios
      .post("https://41352fc471fa.ngrok.io/vsigverify", fd, {
        headers: {
          "Content-Type": "multipart/form-data",
          enctype: "multipart/form-data",
        },
      })
      .then(async (res) => {
        const { result } = res.data;
        console.log(res.data);
        if (result) {
          setSuccess(true);
        } else {
          setSuccess(false);
        }
      });
  };

  if (typeof window === "undefined" || !process.browser) return null;

  return (
    <div ref={wrapperRef}>
      <div className='flex items-center'>
        <h1 className='text-left text-3xl text-blue-800 font-bold mb-4'>
          Voice Signature
        </h1>
        {success ? (
          <span className='ml-4 font-bold text-green-500 mb-2'>
            <CheckCircleIcon className='inline-block w-6 h-6 mb-[3px] mr-1 text-green-500' />
            Voice Signature Verified.
          </span>
        ) : (
          <span className='ml-4 font-bold text-red-500 mb-2'>
            <XCircleIcon className='inline-block w-6 h-6 mb-[3px] mr-1 text-red-500' />
            Voice Signature Not Verified.
          </span>
        )}
      </div>
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
