
import React from 'react';
import { Link } from 'react-router-dom';

const Hero = () => {
  return (
    <div className="relative bg-gradient-to-br from-green-800 via-green-700 to-green-600 text-white">
      <div className="absolute inset-0 bg-black opacity-10"></div>
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
        <div className="text-center">
          {/* Party Logo */}
          <div className="mb-8">
            <img 
              src="/lovable-uploads/logo.png" 
              alt="People Unite for Change Logo" 
              className="w-24 h-24 mx-auto object-contain"
            />
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight font-century-gothic">
            Welcome to the website of <span className="text-yellow-400 font-arcon">People Unite for Change</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-4xl mx-auto leading-relaxed font-century-gothic">
            A Movement About The Government is now for the People by the People
          </p>
          
          {/* President Section */}
          <div className="bg-white text-gray-800 rounded-lg p-8 mt-12 max-w-md mx-auto">
            <h2 className="text-2xl font-bold text-green-800 mb-4 font-century-gothic">President</h2>
            <div className="w-32 h-32 bg-blue-200 rounded-full mx-auto mb-4 flex items-center justify-center">
              <div className="w-24 h-24 bg-blue-300 rounded-full"></div>
            </div>
            <h3 className="font-semibold text-lg mb-2 font-century-gothic">Candidate Name Here</h3>
            <p className="text-sm text-gray-600 font-century-gothic">Party Leader & Presidential Candidate</p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
            <Link
              to="/about"
              className="bg-yellow-500 text-green-900 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-yellow-400 transition-colors duration-200 shadow-lg font-century-gothic"
            >
              Learn About Us
            </Link>
            <Link
              to="/register"
              className="bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-white hover:text-green-900 transition-colors duration-200 font-century-gothic"
            >
              Join Our Movement
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
