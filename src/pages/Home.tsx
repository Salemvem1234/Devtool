
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Users, Award, Star } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-orange-100 to-yellow-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <div className="relative">
                <BookOpen size={80} className="text-red-600" />
                <div className="absolute -top-2 -right-2 bg-yellow-400 rounded-full p-2">
                  <Star size={24} className="text-orange-600" />
                </div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Welcome
            </h1>
            <h2 className="text-3xl md:text-4xl font-semibold text-red-600 mb-6">
              Learn Phonics the Fun Way!
            </h2>
            <p className="text-xl text-gray-700 mb-8 max-w-3xl mx-auto leading-relaxed">
              Where quality teaching and lesson planning of Axaphonics will take place. 
              Our balance reading learning provides fun and effective programs designed to build
              strong foundations in reading through engaging lessons and activities.
            </p>
            
            <Link to="/services">
              <Button size="lg" className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 text-lg rounded-full shadow-lg transform hover:scale-105 transition-all duration-200">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose Axaphonics?</h2>
            <p className="text-lg text-gray-600">Discover the benefits of our proven phonics approach</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center hover:shadow-lg transition-shadow duration-300">
              <CardHeader>
                <div className="mx-auto bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                  <BookOpen className="text-red-600" size={32} />
                </div>
                <CardTitle className="text-xl text-gray-900">Quality Teaching</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Expert-designed curriculum that makes learning phonics engaging and effective for all age groups.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow duration-300">
              <CardHeader>
                <div className="mx-auto bg-yellow-100 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                  <Users className="text-yellow-600" size={32} />
                </div>
                <CardTitle className="text-xl text-gray-900">All Ages Welcome</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  From early learners to teenagers, our programs are tailored to meet every student's needs.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow duration-300">
              <CardHeader>
                <div className="mx-auto bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                  <Award className="text-green-600" size={32} />
                </div>
                <CardTitle className="text-xl text-gray-900">Proven Results</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Our balanced approach to reading has helped thousands of students build strong foundations.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-red-600 to-red-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Start Your Phonics Journey?
          </h2>
          <p className="text-xl text-red-100 mb-8">
            Join thousands of students who have improved their reading skills with Axaphonics
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/services">
              <Button size="lg" variant="secondary" className="bg-white text-red-600 hover:bg-gray-100 px-8 py-3">
                View Services
              </Button>
            </Link>
            <Link to="/contact">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-red-600 px-8 py-3">
                Contact Us
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
