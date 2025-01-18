import React, { useState, useEffect } from 'react';
import { Button, Card, Spacer } from '@nextui-org/react';
import Duck from './components/Duck';
import Chat from './components/Chat';
import Webcam from 'react-webcam';

function App() {
  const [emotion, setEmotion] = useState('');
  const [drowsiness, setDrowsiness] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const [image, setImage] = useState<string | null>(null);

  const analyzeImage = async () => {
    if (!image) return;

    const response = await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });

    const data = await response.json();
    setEmotion(data.emotion);
    setDrowsiness(data.drowsiness);

    // Add emotion and drowsiness to chat
    setMessages(prev => [
      ...prev,
      `Emotion: ${data.emotion}`,
      `Drowsiness: ${data.drowsiness}`,
    ]);
  };

  const roastUser = async () => {
    if (!image) return;

    const response = await fetch('http://localhost:5000/roast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });

    const data = await response.json();
    setMessages(prev => [...prev, `Roast: ${data.roast}`]);
  };

  useEffect(() => {
    console.log("hi")
  }, []);

  return (
    <div style={{ display: 'flex', padding: '20px' }}>
      <Duck emotion={emotion} />
      <Spacer x={2} />
      <Card style={{ width: '300px', padding: '20px' }}>
        <Webcam/>
        <Chat messages={messages} />
        <Spacer y={1} />
        <Button onClick={analyzeImage}>Analyze Emotion</Button>
        <Spacer y={1} />
        <Button onClick={roastUser}>Roast Me</Button>
      </Card>
    </div>
  );
}

export default App;