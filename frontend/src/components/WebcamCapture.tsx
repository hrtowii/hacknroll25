import React from 'react';
import Webcam from 'react-webcam';
import { Card } from "@nextui-org/react";

interface WebcamCaptureProps {
  webcamRef: React.RefObject<Webcam>; // Pass the ref from the parent
  onEmotionDetected?: (emotion: string) => void; // Optional callback
}

export const WebcamCapture: React.FC<WebcamCaptureProps> = ({ webcamRef, onEmotionDetected }) => {
  return (
    <Card className="p-2" style={{ visibility: 'hidden', position: 'absolute' }}>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/Sjpeg"
        width={1920}
        height={1080}
      />
    </Card>
  );
};