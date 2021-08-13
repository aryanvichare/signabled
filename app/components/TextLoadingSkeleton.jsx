import React from "react";

const TextLoadingSkeleton = () => {
  return (
    <>
      {Array.from({ length: 12 }, (_, i) => i + 1).map((_, idx) => (
        <div
          key={idx}
          className='w-full h-5 bg-gray-200 animate-pulse mb-3 rounded'
        />
      ))}
    </>
  );
};

export default TextLoadingSkeleton;
