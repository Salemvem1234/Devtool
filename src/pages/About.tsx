
import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold text-center mb-4">
            About People Unite for Change
          </h1>
          <p className="text-xl text-center max-w-3xl mx-auto">
            Discover our story, mission, and vision for a better Namibia
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid lg:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Story</h2>
            <p className="text-gray-600 mb-4">
              People Unite for Change was founded in 2024 as a response to the growing need for 
              fresh perspectives and innovative solutions in Namibian politics. Born from grassroots 
              movements across the country, our party represents the voice of citizens who believe 
              in the power of unity and democratic change.
            </p>
            <p className="text-gray-600 mb-4">
              We emerged from town halls, community gatherings, and conversations with ordinary 
              Namibians who shared a common vision: a country where every citizen has equal 
              opportunities, where transparency guides governance, and where progress benefits all.
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-white font-bold text-3xl">P</span>
            </div>
            <h3 className="text-xl font-semibold text-center text-gray-900 mb-4">Party Logo</h3>
            <p className="text-gray-600 text-center">
              Our logo represents unity, progress, and the collective strength of the Namibian people.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h3>
            <p className="text-gray-600">
              To serve as a catalyst for positive change in Namibia by promoting democratic values, 
              ensuring transparent governance, and implementing policies that create opportunities 
              for all citizens to thrive and contribute to our nation's development.
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Our Vision</h3>
            <p className="text-gray-600">
              A prosperous, united, and equitable Namibia where every citizen enjoys equal rights, 
              opportunities, and access to quality education, healthcare, and economic participation, 
              while preserving our natural heritage for future generations.
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Why We Were Formed</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">💡</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Innovation</h4>
              <p className="text-gray-600 text-sm">
                Bringing fresh ideas and modern solutions to traditional challenges
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">👥</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Representation</h4>
              <p className="text-gray-600 text-sm">
                Ensuring all voices are heard in the democratic process
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">🎯</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Accountability</h4>
              <p className="text-gray-600 text-sm">
                Maintaining transparency and responsibility in all our actions
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
