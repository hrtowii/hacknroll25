import { useState, useEffect, useCallback, useRef } from 'react';
import { NextUIProvider, Button } from "@nextui-org/react";
import Webcam from 'react-webcam';
import { ChatMessage } from './components/Chat';
import Duck from './components/Duck';
import { BackendUrl } from './utils/BackendUrl';
import { WebcamCapture } from './components/WebcamCapture';

interface Message {
  text: string;
  isAI: boolean;
}

function App() {
  const [emotion, setEmotion] = useState('');
  const [drowsiness, setDrowsiness] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hey there! I'm your personal roasting AI. Turn on your camera so I can see your beautiful face and roast you properly! 😈", isAI: true }
  ]);
  const [image, setImage] = useState<string | null>(null);
  const [isCapturing, setIsCapturing] = useState(true); // Track whether capturing is active
  const webcamRef = useRef<any>(null);

  // Capture function to get screenshot from webcam
  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc); // Save the captured image
      console.log("Image captured:", imageSrc);
    } else {
      console.error("Webcam ref is not set");
    }
  }, [webcamRef]);

  // Effect to handle periodic capturing
  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | null = null;

    if (isCapturing) {
      timer = setInterval(() => {
        console.log("Capturing image...");
        capture();
      }, 5000); // Capture every 5 seconds
    }

    return () => {
      if (timer) {
        clearInterval(timer);
      }
    };
  }, [isCapturing, capture]);

  const roastUser = async () => {
    if (!image) return;

    const response = await fetch(`${BackendUrl}/roast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });

    const data = await response.json();
    setMessages(prev => [...prev, { text: `Roast: ${data.roast}`, isAI: true }]);
  };

  const analyzeImage = async () => {
    if (!image) return;

    const response = await fetch(`${BackendUrl}/detect`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frame: image.split(',')[1] }),
    });

    const data = await response.json();
    console.log(data)
    setEmotion(data.emotion);
    // setDrowsiness(data.drowsiness);

    // Append the emotion and remark to the chat messages
    setMessages(prev => [
      ...prev,
      { text: `Emotion: ${data.emotion}, Remark: ${data.remark}`, isAI: true }
    ]);
  };

  return (
    <NextUIProvider>
      <div className="min-h-screen bg-gradient-to-br from-yellow-500 to-orange-800 p-4">
        <div className="flex flex-col items-center gap-4">

          <WebcamCapture webcamRef={webcamRef}/>
          {/* Duck Component */}
          <Duck emotion={emotion} />

          {/* Message Area */}
          <div className="bg-white rounded-2xl p-4 shadow-lg flex flex-col w-full">
            <div className="flex-1 overflow-y-auto space-y-4 p-4">
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message.text} isAI={message.isAI} emotion={emotion} />
              ))}
            </div>
          </div>

          {/* Buttons to Analyze Image and Roast */}
          <div className="flex flex-col gap-4 w-full mt-4">
            <Button onClick={analyzeImage} className="w-full">Analyze Emotion</Button>
            <Button onClick={roastUser} className="w-full">Roast Me</Button>
          </div>

          {/* Emotion Display */}
          <div className="bg-white rounded-2xl p-4 shadow-lg w-full mt-4">
            <h3 className="text-lg font-semibold mb-2">Current Emotion</h3>
            <p className="text-gray-600">{emotion || 'Waiting for emotion detection...'}</p>
          </div>
        </div>
      </div>
    </NextUIProvider>
  );
}

export default App;