
import React from 'react';
import { Mail, Phone, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">P</span>
              </div>
              <span className="font-bold text-xl">People Unite for Change</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              Building a stronger, more unified Namibia through democratic values, 
              transparency, and progressive policies that serve all citizens.
            </p>
            <div className="space-y-2">
              <div className="flex items-center">
                <Phone size={16} className="mr-2 text-blue-400" />
                <span className="text-gray-300">+264 61 123 4567</span>
              </div>
              <div className="flex items-center">
                <Mail size={16} className="mr-2 text-blue-400" />
                <span className="text-gray-300">info@peopleuniteforchange.na</span>
              </div>
              <div className="flex items-center">
                <MapPin size={16} className="mr-2 text-blue-400" />
                <span className="text-gray-300">Windhoek, Namibia</span>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="font-semibold text-lg mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-300 hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/about" className="text-gray-300 hover:text-white transition-colors">About Us</Link></li>
              <li><Link to="/documents" className="text-gray-300 hover:text-white transition-colors">Documents</Link></li>
              <li><Link to="/media" className="text-gray-300 hover:text-white transition-colors">Media</Link></li>
              <li><Link to="/contact" className="text-gray-300 hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-lg mb-4">Get Involved</h3>
            <ul className="space-y-2">
              <li><Link to="/register" className="text-gray-300 hover:text-white transition-colors">Register as Member</Link></li>
              <li><Link to="/volunteer" className="text-gray-300 hover:text-white transition-colors">Volunteer</Link></li>
              <li><Link to="/donate" className="text-gray-300 hover:text-white transition-colors">Support Us</Link></li>
              <li><Link to="/events" className="text-gray-300 hover:text-white transition-colors">Events</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400">
            © 2024 People Unite for Change. All rights reserved. | 
            <Link to="/privacy" className="hover:text-white ml-1">Privacy Policy</Link> | 
            <Link to="/terms" className="hover:text-white ml-1">Terms of Service</Link>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
