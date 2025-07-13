
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Mail, Phone, MapPin, Clock, Facebook, Twitter, Instagram } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate form submission
    toast({
      title: "Message Sent!",
      description: "Thank you for your message. We'll get back to you soon.",
    });
    setFormData({ name: '', email: '', message: '' });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50">
      {/* Header Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">Contact Us</h1>
            <p className="text-xl text-gray-700 max-w-3xl mx-auto">
              Get in touch with us to learn more about our phonics programs or to schedule a consultation
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <Card className="shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl text-gray-900">Send us a Message</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <Label htmlFor="name" className="text-gray-700">Your Name</Label>
                    <Input
                      id="name"
                      name="name"
                      type="text"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      className="mt-1"
                      placeholder="Enter your full name"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="email" className="text-gray-700">Your Email</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="mt-1"
                      placeholder="Enter your email address"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="message" className="text-gray-700">Your Message</Label>
                    <Textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      required
                      className="mt-1 min-h-[120px]"
                      placeholder="Tell us about your needs or ask any questions..."
                    />
                  </div>
                  
                  <Button 
                    type="submit" 
                    className="w-full bg-red-600 hover:bg-red-700 text-white py-3 text-lg"
                  >
                    Send Message
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Contact Information */}
            <div className="space-y-8">
              <Card className="shadow-lg">
                <CardHeader>
                  <CardTitle className="text-2xl text-gray-900">Reach Us Through</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className="bg-red-100 w-12 h-12 rounded-full flex items-center justify-center">
                      <Mail className="text-red-600" size={24} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Email</h3>
                      <p className="text-gray-600">axaphonics@gmail.com</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center">
                      <Phone className="text-blue-600" size={24} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Phone</h3>
                      <p className="text-gray-600">Phone: 72 (0) 11 516 1966</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center">
                      <MapPin className="text-green-600" size={24} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Location</h3>
                      <p className="text-gray-600">Johannesburg, South Africa</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="bg-purple-100 w-12 h-12 rounded-full flex items-center justify-center">
                      <Clock className="text-purple-600" size={24} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Office Hours</h3>
                      <p className="text-gray-600">Mon - Fri: 9:00 AM - 5:00 PM</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="shadow-lg">
                <CardHeader>
                  <CardTitle className="text-2xl text-gray-900">Social Network</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <a 
                      href="#" 
                      className="flex items-center space-x-4 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="bg-blue-100 w-10 h-10 rounded-full flex items-center justify-center">
                        <Facebook className="text-blue-600" size={20} />
                      </div>
                      <span className="text-gray-700 font-medium">axaphonics.edu</span>
                    </a>
                    
                    <a 
                      href="#" 
                      className="flex items-center space-x-4 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="bg-blue-100 w-10 h-10 rounded-full flex items-center justify-center">
                        <Twitter className="text-blue-400" size={20} />
                      </div>
                      <span className="text-gray-700 font-medium">@axaphonics</span>
                    </a>
                    
                    <a 
                      href="#" 
                      className="flex items-center space-x-4 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="bg-pink-100 w-10 h-10 rounded-full flex items-center justify-center">
                        <Instagram className="text-pink-600" size={20} />
                      </div>
                      <span className="text-gray-700 font-medium">axaphonics_official</span>
                    </a>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;
