
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Award, BookOpen, Users, Target, Heart, Star } from 'lucide-react';

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50">
      {/* Header Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">About Veronica V.Axakhoes</h1>
            <p className="text-xl text-gray-700 max-w-3xl mx-auto">
              Dedicated educator and phonics specialist with a passion for helping students achieve reading success
            </p>
          </div>

          {/* Profile Section */}
          <div className="grid lg:grid-cols-2 gap-12 mb-16">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex items-center mb-6">
                <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mr-4">
                  <BookOpen className="text-red-600" size={32} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Mrs V.Axakhoes</h2>
                  <p className="text-gray-600">Founder & Lead Educator</p>
                </div>
              </div>
              
              <p className="text-gray-700 mb-6 leading-relaxed">
                With over 15 years of experience in phonics education, Mrs. V.Axakhoes has dedicated her career to 
                developing innovative teaching methods that make learning to read both effective and enjoyable. Her 
                approach combines traditional phonics principles with modern educational techniques.
              </p>
              
              <p className="text-gray-700 leading-relaxed">
                She holds advanced certifications in reading instruction and has helped thousands of students 
                overcome reading challenges while building confidence in their literacy skills.
              </p>
            </div>

            <div className="space-y-6">
              <Card className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center text-xl">
                      <Award className="text-yellow-600 mr-3" size={24} />
                      Qualifications
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex items-center">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                      Master's in Education (Reading Specialist)
                    </li>
                    <li className="flex items-center">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                      Certified Phonics Instructor
                    </li>
                    <li className="flex items-center">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                      Special Needs Education Certificate
                    </li>
                    <li className="flex items-center">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                      15+ Years Teaching Experience
                    </li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center text-xl">
                    <Star className="text-yellow-600 mr-3" size={24} />
                    Specializations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    <Badge className="bg-blue-500">Early Childhood</Badge>
                    <Badge className="bg-green-500">Remedial Reading</Badge>
                    <Badge className="bg-purple-500">Adult Literacy</Badge>
                    <Badge className="bg-orange-500">Special Needs</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Mission & Vision */}
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            <Card className="bg-gradient-to-br from-red-50 to-red-100 border-red-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center text-2xl text-red-800">
                  <Target className="mr-3" size={28} />
                  Our Mission
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-red-700 leading-relaxed">
                  To provide exceptional phonics education that empowers students of all ages to become confident, 
                  fluent readers. We believe that strong reading foundations open doors to lifelong learning and success.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-yellow-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center text-2xl text-yellow-800">
                  <Heart className="mr-3" size={28} />
                  Our Approach
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-yellow-700 leading-relaxed">
                  We combine proven phonics methods with personalized attention, ensuring each student receives 
                  the support they need to succeed. Our patient, encouraging approach builds both skills and confidence.
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Stats Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Our Impact</h2>
            <div className="grid md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="text-blue-600" size={32} />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">2,500+</div>
                <p className="text-gray-600">Students Taught</p>
              </div>
              
              <div>
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BookOpen className="text-green-600" size={32} />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">15</div>
                <p className="text-gray-600">Years Experience</p>
              </div>
              
              <div>
                <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Award className="text-purple-600" size={32} />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">98%</div>
                <p className="text-gray-600">Success Rate</p>
              </div>
              
              <div>
                <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Star className="text-orange-600" size={32} />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">50+</div>
                <p className="text-gray-600">Programs Developed</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
