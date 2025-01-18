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

  return (
    <div style={{ width: '45px', height: '45px', overflow: 'hidden' }}>
      <img
        src={`./assets/images/logo.png`}
        alt="Duck"
        style={{ transform: `rotate(${rotation}deg)`, height: '100%', width: '100%' }}
      />
    </div>
  );
};

export default Duck;