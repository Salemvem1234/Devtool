
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Mail, Phone, MapPin, Send, MessageCircle } from 'lucide-react';
import { useState } from 'react';

const Contact = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    message: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    // Handle form submission here
  };

  return (
    <div className="page-container">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="hero-section mb-12">
          <h1 className="text-6xl md:text-7xl font-bold text-foreground mb-6">
            Contact Us
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
            Ready to start your phonics journey? We'd love to hear from you! Get in touch to learn more about our programs and how we can help you or your child succeed.
          </p>
        </div>

        {/* Contact Form and Info */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8 text-center">Get In Touch</h2>
          
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <Card className="bg-card border-2 border-border">
              <CardHeader>
                <CardTitle className="text-2xl text-foreground flex items-center gap-3">
                  <MessageCircle className="w-6 h-6 text-primary" />
                  Send us a message
                </CardTitle>
                <p className="text-muted-foreground text-lg">Fill out the form below and we'll get back to you within 24 hours.</p>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="firstName" className="text-foreground text-lg font-medium">First Name</Label>
                      <Input
                        id="firstName"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        className="mt-2 bg-background border-2 border-border text-lg py-3"
                        placeholder="Enter your first name"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="lastName" className="text-foreground text-lg font-medium">Last Name</Label>
                      <Input
                        id="lastName"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        className="mt-2 bg-background border-2 border-border text-lg py-3"
                        placeholder="Enter your last name"
                        required
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="email" className="text-foreground text-lg font-medium">Email Address</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="mt-2 bg-background border-2 border-border text-lg py-3"
                      placeholder="Enter your email address"
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="message" className="text-foreground text-lg font-medium">Message</Label>
                    <textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      rows={5}
                      className="mt-2 w-full px-4 py-3 bg-background border-2 border-border rounded-md text-foreground text-lg placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                      placeholder="Tell us about your phonics learning needs..."
                      required
                    />
                  </div>
                  
                  <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-4 text-lg font-semibold">
                    <Send className="w-5 h-5 mr-2" />
                    Send Message
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Contact Information */}
            <div className="space-y-8">
              <Card className="bg-card border-2 border-border">
                <CardHeader>
                  <CardTitle className="text-2xl text-foreground">Contact Information</CardTitle>
                  <p className="text-muted-foreground text-lg">Reach out to us through any of these channels</p>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-primary/10 rounded-full">
                      <Mail className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground font-medium">Email Address</p>
                      <p className="text-foreground font-semibold text-lg">axaphonics@gmail.com</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-secondary/30 rounded-full">
                      <Phone className="w-6 h-6 text-secondary-foreground" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground font-medium">Phone Number</p>
                      <p className="text-foreground font-semibold text-lg">+27 (0) 11 234 5678</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-card border-2 border-border">
                <CardHeader>
                  <CardTitle className="text-2xl text-foreground">Online Presence</CardTitle>
                  <p className="text-muted-foreground text-lg">Connect with us on social media</p>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-accent rounded-full"></div>
                    <span className="text-foreground text-lg">axaphonics.co.za</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-accent rounded-full"></div>
                    <span className="text-foreground text-lg">facebook.com/axaphonics</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-accent rounded-full"></div>
                    <span className="text-foreground text-lg">instagram.com/axaphonics</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-secondary/20 to-accent/20 border-2 border-border text-center">
                <CardContent className="pt-8 pb-8">
                  <h3 className="text-2xl font-bold text-foreground mb-4">Ready to Start Learning?</h3>
                  <p className="text-muted-foreground text-lg mb-6">
                    Contact us today to begin your phonics education journey with expert guidance and personalized support.
                  </p>
                  <Button className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 text-lg font-semibold">
                    Schedule a Consultation
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="hero-section bg-gradient-to-r from-muted/30 to-card">
          <h2 className="text-4xl font-bold text-foreground mb-6">
            Frequently Asked Questions
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-4xl mx-auto">
            Have questions about our programs? We're here to help! Contact us for detailed information about our phonics education methods, scheduling, and enrollment process.
          </p>
          <Button size="lg" variant="outline" className="border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground px-10 py-4 text-xl font-semibold">
            View FAQ
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Contact;
