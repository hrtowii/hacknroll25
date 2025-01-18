import React, { useState, useRef } from 'react';
import { NextUIProvider } from "@nextui-org/react";
import { Card } from "@nextui-org/react";
import Webcam from 'react-webcam';
import { Truck as Duck } from 'lucide-react';

function App() {
  const [duckMessage, setDuckMessage] = useState("Oh look who decided to show up... 😏");
  const webcamRef = useRef<Webcam>(null);

  const captureEmotion = async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      // TODO: Send to backend for emotion processing
      const mockMessages = [
        "Is that your actual face or are you wearing a mask? 🤔",
        "You look like you're having a rough day... good. 😈",
        "Did someone tell you that expression suits you? They lied. 🦆",
        "I've seen potatoes with more personality! 🥔",
        "Oh, you're still here? Persistent, aren't we? 🙄",
        "That's an... interesting choice of facial expression. 😬"
      ];
      setDuckMessage(mockMessages[Math.floor(Math.random() * mockMessages.length)]);
    }
  };

  React.useEffect(() => {
    const interval = setInterval(captureEmotion, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <NextUIProvider>
      <div className="min-h-screen bg-gradient-to-br from-purple-100 to-blue-100 flex">
        {/* Main Content Area */}
        {/* <div className="flex-1 p-4 flex items-center justify-center">
          <Card className="p-6 max-w-md">
            <h1 className="text-2xl font-bold mb-4">Welcome to Your Personal Roast Session</h1>
            <p className="text-gray-600">
              Just sit back and let our AI-powered duck judge your every expression. 
              Don't worry, it's totally not storing these images... maybe. 😈
            </p>
          </Card>
        </div> */}

        {/* Duck Sidebar */}
        <div className="w-64 bg-white shadow-lg flex flex-col">
          <div className="p-4 flex flex-col items-center sticky top-0">
            <div className="relative">
              <Duck 
                size={48} 
                className="text-yellow-500 mb-4 animate-bounce" 
              />
            </div>
            <Card className="w-full p-3 bg-yellow-50 transition-all duration-300 hover:scale-105">
              <p className="text-sm font-medium">{duckMessage}</p>
            </Card>
          </div>
        </div>

        {/* Hidden Webcam */}
        <div className="hidden">
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={{
              width: 320,
              height: 240,
              facingMode: "user"
            }}
          />
        </div>
      </div>
    </NextUIProvider>
  );
}

export default App;