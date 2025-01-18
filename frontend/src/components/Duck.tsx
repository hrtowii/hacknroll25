import React, { useEffect, useState } from 'react';

interface DuckProps {
  emotion?: string;
}

const Duck = ({ emotion }: DuckProps) => {
  const [rotation, setRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRotation(prev => (prev + 10) % 360);
    }, 100);
    return () => clearInterval(interval);
  }, []);

let assets = ['./assets/images/logo.png','./assets/images/angrylogo.png','./assets/images/happylogo.png','./assets/images/sadlogo.png','./assets/images/scaredlogo.png']
  return (
    <div style={{ width: '45px', height: '45px', overflow: 'hidden' }}>
      <img
        src={emotion == 'neutral'?assets[0]:emotion == 'angry'?assets[1]:emotion == 'happy'?assets[2]:emotion == 'sad'?assets[3]:emotion == 'fear'?assets[4]:assets[0]}
            
        alt="Duck"
        style={{ transform: `rotate(${rotation}deg)`, height: '100%', width: '100%' }}
      />
    </div>
  );
};

export default Duck;