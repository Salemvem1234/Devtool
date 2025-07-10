
import React, { useState } from 'react';
import { Menu, X, Search, Facebook, Twitter, Instagram, Youtube } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Input } from '@/components/ui/input';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Documents', path: '/documents' },
    { name: 'Media', path: '/media' },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' },
  ];

  const socialLinks = [
    { name: 'Facebook', icon: Facebook, url: '#' },
    { name: 'Twitter', icon: Twitter, url: '#' },
    { name: 'Instagram', icon: Instagram, url: '#' },
    { name: 'YouTube', icon: Youtube, url: '#' },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Search query:', searchQuery);
    // Add search functionality here
  };

  return (
    <div className="font-calibri">
      {/* Top bar with social media and search */}
      <div className="bg-green-700 py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            {/* Social Media Links */}
            <div className="hidden md:flex items-center space-x-4">
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.url}
                  className="text-white hover:text-yellow-400 transition-colors duration-200"
                  aria-label={social.name}
                >
                  <social.icon size={18} />
                </a>
              ))}
            </div>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="flex items-center">
              <div className="relative">
                <Input
                  type="text"
                  placeholder="Search..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-64 pr-10 h-8 text-sm bg-white border-none focus:ring-1 focus:ring-yellow-400"
                />
                <button
                  type="submit"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  <Search size={16} />
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="bg-green-800 shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-3">
                <img 
                  src="/lovable-uploads/8c558d27-8d21-4b3e-99dc-bfe0ccf75a78.png" 
                  alt="People Unite for Change Logo" 
                  className="w-12 h-12 object-contain"
                />
                <span className="font-bold text-2xl text-white">People Unite for Change</span>
              </Link>
            </div>
            
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-6">
                {navItems.map((item) => (
                  <Link
                    key={item.name}
                    to={item.path}
                    className="text-white hover:text-yellow-400 px-3 py-2 rounded-md text-lg font-medium transition-colors duration-200"
                  >
                    {item.name}
                  </Link>
                ))}
                <Link
                  to="/register"
                  className="bg-yellow-500 text-green-800 px-4 py-2 rounded-md text-base font-medium hover:bg-yellow-400 transition-colors duration-200 font-bold"
                >
                  Click to Register
                </Link>
              </div>
            </div>
            
            <div className="md:hidden">
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="text-white hover:text-yellow-400 focus:outline-none focus:text-yellow-400"
              >
                {isOpen ? <X size={28} /> : <Menu size={28} />}
              </button>
            </div>
          </div>
        </div>

        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-green-800 shadow-lg">
              {/* Mobile Social Links */}
              <div className="flex justify-center space-x-6 py-3 border-b border-green-700 mb-3">
                {socialLinks.map((social) => (
                  <a
                    key={social.name}
                    href={social.url}
                    className="text-white hover:text-yellow-400 transition-colors duration-200"
                    aria-label={social.name}
                  >
                    <social.icon size={20} />
                  </a>
                ))}
              </div>
              
              {/* Mobile Search */}
              <div className="px-3 py-2">
                <form onSubmit={handleSearch} className="relative">
                  <Input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pr-10 h-10 bg-white border-none focus:ring-1 focus:ring-yellow-400"
                  />
                  <button
                    type="submit"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    <Search size={18} />
                  </button>
                </form>
              </div>

              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.path}
                  className="text-white hover:text-yellow-400 block px-3 py-2 rounded-md text-lg font-medium"
                  onClick={() => setIsOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              <Link
                to="/register"
                className="bg-yellow-500 text-green-800 block px-3 py-2 rounded-md text-base font-medium hover:bg-yellow-400 transition-colors duration-200 mt-4 font-bold"
                onClick={() => setIsOpen(false)}
              >
                Click to Register
              </Link>
            </div>
          </div>
        )}
      </nav>
    </div>
  );
};

export default Navbar;
