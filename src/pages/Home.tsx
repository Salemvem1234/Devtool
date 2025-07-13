
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Users, Award, Star, Heart, GraduationCap } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="page-container">
      {/* Hero Section - Matching reference design */}
      <section className="py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="hero-section">
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="w-24 h-24 bg-primary/20 rounded-full flex items-center justify-center">
                  <BookOpen size={48} className="text-primary" />
                </div>
                <div className="absolute -top-2 -right-2 bg-secondary rounded-full p-2">
                  <Star size={20} className="text-secondary-foreground" />
                </div>
              </div>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold text-foreground mb-4">
              Welcome
            </h1>
            <h2 className="text-4xl md:text-5xl font-bold text-primary mb-8">
              Learn Phonics the Fun Way!
            </h2>
            <p className="text-xl text-muted-foreground mb-12 max-w-4xl mx-auto leading-relaxed">
              Where quality teaching and lesson planning of Axaphonics will take place. 
              Our balanced reading learning provides fun and effective programs designed to build
              strong foundations in reading through engaging lessons and activities.
            </p>
            
            <Link to="/services">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-12 py-4 text-xl rounded-full shadow-xl transform hover:scale-105 transition-all duration-200">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section - Precise layout */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="content-section">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-foreground mb-6">Why Choose Axaphonics?</h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Discover the benefits of our proven phonics approach designed for every learner
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              {/* Early Learners Card */}
              <Card className="text-center bg-card border-2 border-border hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                <CardHeader className="pb-4">
                  <div className="mx-auto bg-primary/10 w-20 h-20 rounded-full flex items-center justify-center mb-6">
                    <Heart className="text-primary" size={40} />
                  </div>
                  <CardTitle className="text-2xl text-foreground">Early Learners</CardTitle>
                  <p className="text-lg text-primary font-semibold">Ages 4-6</p>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg leading-relaxed">
                    Foundation phonics program with interactive games and activities that make learning fun and engaging for young children.
                  </p>
                </CardContent>
              </Card>

              {/* Primary School Card */}
              <Card className="text-center bg-card border-2 border-border hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                <CardHeader className="pb-4">
                  <div className="mx-auto bg-secondary/30 w-20 h-20 rounded-full flex items-center justify-center mb-6">
                    <BookOpen className="text-secondary-foreground" size={40} />
                  </div>
                  <CardTitle className="text-2xl text-foreground">Primary School</CardTitle>
                  <p className="text-lg text-secondary-foreground font-semibold">Ages 7-10</p>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg leading-relaxed">
                    Advanced phonics and spelling program that builds on foundation skills with complex reading and writing activities.
                  </p>
                </CardContent>
              </Card>

              {/* Teenagers Card */}
              <Card className="text-center bg-card border-2 border-border hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                <CardHeader className="pb-4">
                  <div className="mx-auto bg-accent/20 w-20 h-20 rounded-full flex items-center justify-center mb-6">
                    <GraduationCap className="text-accent" size={40} />
                  </div>
                  <CardTitle className="text-2xl text-foreground">Teenagers</CardTitle>
                  <p className="text-lg text-accent font-semibold">Ages 11-14</p>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg leading-relaxed">
                    Specialized program for older students who need additional support with reading, spelling, and confidence building.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Results Section */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="content-section">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-foreground mb-6">Proven Results</h2>
              <p className="text-xl text-muted-foreground">
                Our balanced approach has helped thousands of students succeed
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <div className="space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                      <Award className="text-primary" size={24} />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-foreground">15+ Years Experience</h3>
                      <p className="text-muted-foreground">Proven track record in phonics education</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-secondary/30 rounded-full flex items-center justify-center">
                      <Users className="text-secondary-foreground" size={24} />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-foreground">All Ages Welcome</h3>
                      <p className="text-muted-foreground">Tailored programs for every learning stage</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-accent/20 rounded-full flex items-center justify-center">
                      <Star className="text-accent" size={24} />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-foreground">Engaging Methods</h3>
                      <p className="text-muted-foreground">Fun and interactive learning approaches</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-primary/10 to-secondary/20 rounded-2xl p-8 text-center">
                <h3 className="text-3xl font-bold text-primary mb-4">Ready to Begin?</h3>
                <p className="text-xl text-muted-foreground mb-6">
                  Join our community of successful learners today
                </p>
                <Link to="/contact">
                  <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 text-lg">
                    Contact Us Today
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="hero-section bg-gradient-to-r from-primary to-primary/80">
            <h2 className="text-4xl font-bold text-primary-foreground mb-6">
              Ready to Start Your Phonics Journey?
            </h2>
            <p className="text-xl text-primary-foreground/90 mb-10 max-w-3xl mx-auto">
              Join thousands of students who have improved their reading skills with our comprehensive phonics programs
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link to="/services">
                <Button size="lg" variant="secondary" className="bg-white text-primary hover:bg-white/90 px-10 py-4 text-lg font-semibold">
                  View Our Services
                </Button>
              </Link>
              <Link to="/about">
                <Button size="lg" variant="outline" className="border-2 border-white text-white hover:bg-white hover:text-primary px-10 py-4 text-lg font-semibold">
                  Learn More About Us
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
