
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Users, GraduationCap, Baby, School, UserCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

const Services = () => {
  const services = [
    {
      id: 1,
      title: "Early Learners (Ages 4-6)",
      icon: Baby,
      description: "Foundation phonics programs designed specifically for young children beginning their reading journey.",
      features: ["Letter recognition", "Basic sound patterns", "Interactive games", "Story time sessions"],
      color: "bg-blue-100 text-blue-600",
      badgeColor: "bg-blue-500"
    },
    {
      id: 2,
      title: "Primary School (Ages 7-10)",
      icon: School,
      description: "Comprehensive phonics curriculum aligned with primary school reading requirements.",
      features: ["Advanced phonics", "Spelling patterns", "Reading comprehension", "Writing skills"],
      color: "bg-green-100 text-green-600",
      badgeColor: "bg-green-500"
    },
    {
      id: 3,
      title: "Teenagers (Ages 11-16)",
      icon: GraduationCap,
      description: "Specialized programs for older students who need additional reading support.",
      features: ["Complex phonics rules", "Advanced vocabulary", "Study skills", "Exam preparation"],
      color: "bg-purple-100 text-purple-600",
      badgeColor: "bg-purple-500"
    },
    {
      id: 4,
      title: "Adult Learning",
      icon: UserCheck,
      description: "Phonics programs designed for adult learners and literacy development.",
      features: ["Adult-focused content", "Flexible scheduling", "Professional materials", "Career support"],
      color: "bg-orange-100 text-orange-600",
      badgeColor: "bg-orange-500"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50">
      {/* Header Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">Our Services</h1>
            <p className="text-xl text-gray-700 max-w-3xl mx-auto">
              Comprehensive phonics education programs tailored for every age group and learning level
            </p>
          </div>

          {/* Services Grid */}
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            {services.map((service) => {
              const IconComponent = service.icon;
              return (
                <Card key={service.id} className="hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                  <CardHeader>
                    <div className="flex items-center justify-between mb-4">
                      <div className={`w-12 h-12 rounded-full ${service.color} flex items-center justify-center`}>
                        <IconComponent size={24} />
                      </div>
                      <Badge className={`${service.badgeColor} text-white`}>Popular</Badge>
                    </div>
                    <CardTitle className="text-2xl text-gray-900">{service.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-6">{service.description}</p>
                    <div className="space-y-2 mb-6">
                      <h4 className="font-semibold text-gray-900">What's Included:</h4>
                      <ul className="space-y-1">
                        {service.features.map((feature, index) => (
                          <li key={index} className="flex items-center text-gray-600">
                            <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                            {feature}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <Link to="/contact">
                      <Button className="w-full bg-red-600 hover:bg-red-700 text-white">
                        Learn More
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Additional Services */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">Additional Services</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BookOpen className="text-red-600" size={32} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Remedial Teaching</h3>
                <p className="text-gray-600">Specialized support for students who need additional help with reading difficulties.</p>
              </div>
              
              <div className="text-center">
                <div className="bg-yellow-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="text-yellow-600" size={32} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Group Classes</h3>
                <p className="text-gray-600">Interactive group sessions that encourage collaborative learning and peer support.</p>
              </div>
              
              <div className="text-center">
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <GraduationCap className="text-green-600" size={32} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Assessment & Evaluation</h3>
                <p className="text-gray-600">Comprehensive assessment to identify learning needs and track progress.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-red-600 to-red-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
          <p className="text-xl text-red-100 mb-8">Contact us today to discuss which program is right for you</p>
          <Link to="/contact">
            <Button size="lg" variant="secondary" className="bg-white text-red-600 hover:bg-gray-100 px-8 py-3">
              Subscribe Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Services;
