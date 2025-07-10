
import React from 'react';
import Hero from '../components/Hero';
import NewsSection from '../components/NewsSection';

const Home = () => {
  return (
    <div className="min-h-screen">
      <Hero />
      <NewsSection />
      
      {/* Mission Statement Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-green-800 mb-4">
              Our Core Values
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The principles that guide our vision for a better Namibia
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="text-xl font-semibold text-green-800 mb-3">Unity</h3>
              <p className="text-gray-600">
                Bringing all Namibians together regardless of background, fostering national cohesion and shared prosperity.
              </p>
            </div>
            
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚖️</span>
              </div>
              <h3 className="text-xl font-semibold text-green-800 mb-3">Transparency</h3>
              <p className="text-gray-600">
                Open governance, accountable leadership, and clear communication with all citizens of Namibia.
              </p>
            </div>
            
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📈</span>
              </div>
              <h3 className="text-xl font-semibold text-green-800 mb-3">Progress</h3>
              <p className="text-gray-600">
                Innovative solutions for economic growth, education, healthcare, and sustainable development.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Welcome Message Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-green-800 mb-6">
            Welcome Back
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed">
            Thank you for visiting our website. People Unite for Change is committed to 
            building a stronger, more unified Namibia through democratic participation, 
            transparent governance, and policies that serve all citizens. Join us as we 
            work together to create positive change for our nation's future.
          </p>
          <div className="mt-8">
            <button className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors duration-200">
              Get Involved Today
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
