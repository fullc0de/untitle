import React from 'react';

const RoundedButton = ({ children, onClick, fontSize = '18px', padding = '15px 25px', variant = 'primary' }) => {
  const getButtonStyle = () => {
    switch (variant) {
      case 'success':
        return {
          backgroundColor: '#4CAF50',
          hoverColor: '#45a049'
        };
      case 'primary':
        return {
          backgroundColor: '#2196F3',
          hoverColor: '#1976D2'
        };
      default:
        return {
          backgroundColor: '#2196F3',
          hoverColor: '#1976D2'
        };
    }
  };

  const style = getButtonStyle();

  return (
    <button
      className="button"
      onClick={onClick}
      style={{
        backgroundColor: style.backgroundColor,
        color: 'white',
        border: 'none',
        padding: padding,
        fontSize: fontSize,
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease'
      }}
      onMouseOver={(e) => e.target.style.backgroundColor = style.hoverColor}
      onMouseOut={(e) => e.target.style.backgroundColor = style.backgroundColor}
    >
      {children}
    </button>
  );
};

export default RoundedButton; 