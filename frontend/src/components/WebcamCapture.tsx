import React from 'react';
import Webcam from 'react-webcam';
import { Card } from "@nextui-org/react";

interface WebcamCaptureProps {
  onEmotionDetected?: (emotion: string) => void;
}

export const WebcamCapture: React.FC<WebcamCaptureProps> = ({ onEmotionDetected }) => {
  return (
    <Card className="p-2">
      <Webcam
        audio={false}
        mirrored={true}
        className="rounded-lg w-full max-w-[320px]"
      />
    </Card>
  );
};