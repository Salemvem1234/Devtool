
import React from 'react';
import { MapPin, Phone, Mail, Clock } from 'lucide-react';

const Contact = () => {
  const offices = [
    {
      name: "Head Office - Windhoek",
      address: "123 Independence Avenue, Windhoek Central, Windhoek",
      phone: "+264 61 123 4567",
      email: "windhoek@peopleuniteforchange.na",
      hours: "Monday - Friday: 8:00 AM - 5:00 PM"
    },
    {
      name: "Northern Regional Office - Oshakati",
      address: "45 Sam Nujoma Drive, Oshakati",
      phone: "+264 65 987 6543",
      email: "oshakati@peopleuniteforchange.na",
      hours: "Monday - Friday: 8:00 AM - 5:00 PM"
    },
    {
      name: "Southern Regional Office - Keetmanshoop",
      address: "78 Schmelen Street, Keetmanshoop",
      phone: "+264 63 456 7890",
      email: "keetmanshoop@peopleuniteforchange.na",
      hours: "Monday - Friday: 8:00 AM - 5:00 PM"
    },
    {
      name: "Coastal Regional Office - Walvis Bay",
      address: "12 Nangolo Mbumba Street, Walvis Bay",
      phone: "+264 64 321 0987",
      email: "walvisbay@peopleuniteforchange.na",
      hours: "Monday - Friday: 8:00 AM - 5:00 PM"
    },
    {
      name: "Eastern Regional Office - Rundu",
      address: "67 Kavango Road, Rundu",
      phone: "+264 66 654 3210",
      email: "rundu@peopleuniteforchange.na",
      hours: "Monday - Friday: 8:00 AM - 5:00 PM"
    },
    {
      name: "Central Regional Office - Okahandja",
      address: "34 Voortrekker Street, Okahandja",
      phone: "+264 62 789 0123",
      email: "okahandja@peopleuniteforchange.na",
      hours: "Monday - Friday: 8:00 AM - 5:00 PM"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold text-center mb-4">
            Contact Us
          </h1>
          <p className="text-xl text-center max-w-3xl mx-auto">
            Get in touch with our offices across Namibia
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Head Office Featured */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Head Office</h2>
            <p className="text-gray-600">Our main office in the heart of Windhoek</p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <div className="space-y-4">
                <div className="flex items-start">
                  <MapPin className="text-blue-600 mr-3 mt-1" size={20} />
                  <div>
                    <h4 className="font-semibold text-gray-900">Address</h4>
                    <p className="text-gray-600">123 Independence Avenue, Windhoek Central, Windhoek</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <Phone className="text-blue-600 mr-3 mt-1" size={20} />
                  <div>
                    <h4 className="font-semibold text-gray-900">Phone</h4>
                    <p className="text-gray-600">+264 61 123 4567</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <Mail className="text-blue-600 mr-3 mt-1" size={20} />
                  <div>
                    <h4 className="font-semibold text-gray-900">Email</h4>
                    <p className="text-gray-600">info@peopleuniteforchange.na</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <Clock className="text-blue-600 mr-3 mt-1" size={20} />
                  <div>
                    <h4 className="font-semibold text-gray-900">Office Hours</h4>
                    <p className="text-gray-600">Monday - Friday: 8:00 AM - 5:00 PM</p>
                    <p className="text-gray-600">Saturday: 9:00 AM - 1:00 PM</p>
                    <p className="text-gray-600">Sunday: Closed</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-100 rounded-lg p-6">
              <h4 className="font-semibold text-gray-900 mb-4">Send us a Message</h4>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input 
                    type="text" 
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your full name"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input 
                    type="email" 
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="your.email@example.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                  <input 
                    type="text" 
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Message subject"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Message</label>
                  <textarea 
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your message here..."
                  ></textarea>
                </div>
                
                <button 
                  type="submit"
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200 font-medium"
                >
                  Send Message
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Regional Offices */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">Regional Offices</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {offices.slice(1).map((office, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">{office.name}</h3>
                
                <div className="space-y-3">
                  <div className="flex items-start">
                    <MapPin className="text-blue-600 mr-2 mt-1" size={16} />
                    <p className="text-gray-600 text-sm">{office.address}</p>
                  </div>
                  
                  <div className="flex items-center">
                    <Phone className="text-blue-600 mr-2" size={16} />
                    <p className="text-gray-600 text-sm">{office.phone}</p>
                  </div>
                  
                  <div className="flex items-center">
                    <Mail className="text-blue-600 mr-2" size={16} />
                    <p className="text-gray-600 text-sm">{office.email}</p>
                  </div>
                  
                  <div className="flex items-start">
                    <Clock className="text-blue-600 mr-2 mt-1" size={16} />
                    <p className="text-gray-600 text-sm">{office.hours}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Emergency Contact */}
        <div className="mt-12 bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-800 mb-2">Emergency Contact</h3>
          <p className="text-red-700 mb-2">
            For urgent political or security-related matters outside office hours:
          </p>
          <p className="text-red-800 font-medium">Emergency Hotline: +264 81 999 0000</p>
        </div>
      </div>
    </div>
  );
};

export default Contact;
