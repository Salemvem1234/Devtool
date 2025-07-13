
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Users, Award, Star } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="page-container">
      {/* Hero Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-section text-center">
            <div className="flex justify-center mb-8">
              <div className="relative">
                <BookOpen size={80} className="text-primary" />
                <div className="absolute -top-2 -right-2 bg-secondary rounded-full p-2">
                  <Star size={24} className="text-secondary-foreground" />
                </div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6">
              Welcome
            </h1>
            <h2 className="text-3xl md:text-4xl font-semibold text-primary mb-6">
              Learn Phonics the Fun Way!
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
              Where quality teaching and lesson planning of Axaphonics will take place. 
              Our balance reading learning provides fun and effective programs designed to build
              strong foundations in reading through engaging lessons and activities.
            </p>
            
            <Link to="/services">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 text-lg rounded-full shadow-lg">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-section">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-foreground mb-4">Why Choose Axaphonics?</h2>
              <p className="text-lg text-muted-foreground">Discover the benefits of our proven phonics approach</p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              <Card className="text-center bg-card/50 border-2 border-border hover:shadow-lg transition-shadow duration-300">
                <CardHeader>
                  <div className="mx-auto bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                    <BookOpen className="text-primary" size={32} />
                  </div>
                  <CardTitle className="text-xl text-foreground">Quality Teaching</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">
                    Expert-designed curriculum that makes learning phonics engaging and effective for all age groups.
                  </p>
                </CardContent>
              </Card>

              <Card className="text-center bg-card/50 border-2 border-border hover:shadow-lg transition-shadow duration-300">
                <CardHeader>
                  <div className="mx-auto bg-secondary/30 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                    <Users className="text-secondary-foreground" size={32} />
                  </div>
                  <CardTitle className="text-xl text-foreground">All Ages Welcome</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">
                    From early learners to teenagers, our programs are tailored to meet every student's needs.
                  </p>
                </CardContent>
              </Card>

              <Card className="text-center bg-card/50 border-2 border-border hover:shadow-lg transition-shadow duration-300">
                <CardHeader>
                  <div className="mx-auto bg-accent/20 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                    <Award className="text-accent" size={32} />
                  </div>
                  <CardTitle className="text-xl text-foreground">Proven Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">
                    Our balanced approach to reading has helped thousands of students build strong foundations.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-section bg-primary text-center">
            <h2 className="text-3xl font-bold text-primary-foreground mb-4">
              Ready to Start Your Phonics Journey?
            </h2>
            <p className="text-xl text-primary-foreground/90 mb-8">
              Join thousands of students who have improved their reading skills with Axaphonics
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/services">
                <Button size="lg" variant="secondary" className="bg-card text-foreground hover:bg-card/90 px-8 py-3">
                  View Services
                </Button>
              </Link>
              <Link to="/contact">
                <Button size="lg" variant="outline" className="border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary px-8 py-3">
                  Contact Us
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
