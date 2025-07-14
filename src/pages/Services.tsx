
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Users, GraduationCap, Star, Clock, Heart, CheckCircle } from 'lucide-react';

const Services = () => {
  const services = [
    {
      title: "Early Learners Program",
      subtitle: "Ages 4-6",
      description: "Foundation phonics program designed for young children just starting their reading journey. Interactive games and activities make learning fun and engaging.",
      features: ["Letter recognition", "Sound blending", "Simple word formation", "Visual and auditory learning"],
      icon: Heart,
      color: "primary"
    },
    {
      title: "Primary School Program", 
      subtitle: "Ages 7-10",
      description: "Advanced phonics and spelling program that builds on foundation skills with more complex reading and writing activities.",
      features: ["Complex phonics patterns", "Spelling rules", "Reading comprehension", "Writing skills"],
      icon: BookOpen,
      color: "secondary"
    },
    {
      title: "Teenage Support Program",
      subtitle: "Ages 11-14", 
      description: "Specialized program for older students who need additional support with reading and spelling skills.",
      features: ["Literacy development", "Study skills", "Confidence building", "Exam preparation"],
      icon: GraduationCap,
      color: "accent"
    }
  ];

  return (
    <div className="page-container">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="hero-section mb-12">
          <h1 className="text-6xl md:text-7xl font-bold text-foreground mb-6">
            Our Services
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
            We offer comprehensive phonics education programs tailored for different age groups and learning needs. 
            Our structured approach ensures effective learning outcomes for every student.
          </p>
        </div>

        {/* Services Grid */}
        <div className="space-y-12">
          {services.map((service, index) => (
            <div key={index} className="content-section">
              <Card className="bg-card border-2 border-border overflow-hidden">
                <CardHeader className="bg-gradient-to-r from-card to-muted/50 pb-8">
                  <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                    <div className={`p-4 rounded-full ${
                      service.color === 'primary' ? 'bg-primary/10' :
                      service.color === 'secondary' ? 'bg-secondary/30' :
                      'bg-accent/20'
                    }`}>
                      <service.icon className={`w-12 h-12 ${
                        service.color === 'primary' ? 'text-primary' :
                        service.color === 'secondary' ? 'text-secondary-foreground' :
                        'text-accent'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-3xl text-foreground mb-2">{service.title}</CardTitle>
                      <p className={`text-xl font-bold mb-3 ${
                        service.color === 'primary' ? 'text-primary' :
                        service.color === 'secondary' ? 'text-secondary-foreground' :
                        'text-accent'
                      }`}>{service.subtitle}</p>
                      <p className="text-muted-foreground text-lg leading-relaxed">{service.description}</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-8">
                  <div className="grid md:grid-cols-2 gap-6 mb-8">
                    {service.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center gap-3">
                        <CheckCircle className="w-5 h-5 text-secondary flex-shrink-0" />
                        <span className="text-foreground text-lg">{feature}</span>
                      </div>
                    ))}
                  </div>
                  <Button 
                    className={`w-full md:w-auto px-8 py-3 text-lg ${
                      service.color === 'primary' ? 'bg-primary hover:bg-primary/90' :
                      service.color === 'secondary' ? 'bg-secondary hover:bg-secondary/90' :
                      'bg-accent hover:bg-accent/90'
                    } text-white`}
                  >
                    Learn More About This Program
                  </Button>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>

        {/* Additional Services */}
        <div className="content-section mt-16">
          <h2 className="text-4xl font-bold text-foreground mb-8 text-center">Additional Services</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <Card className="bg-card border-2 border-border">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <Users className="w-8 h-8 text-primary" />
                  <CardTitle className="text-2xl">Group Classes</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-lg mb-6 leading-relaxed">
                  Small group sessions that encourage peer learning and social interaction while maintaining personalized attention.
                </p>
                <Button variant="outline" className="border-primary text-primary hover:bg-primary hover:text-primary-foreground px-6 py-2">
                  Join a Group Class
                </Button>
              </CardContent>
            </Card>

            <Card className="bg-card border-2 border-border">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <Clock className="w-8 h-8 text-secondary-foreground" />
                  <CardTitle className="text-2xl">Flexible Scheduling</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-lg mb-6 leading-relaxed">
                  We offer flexible scheduling options to accommodate busy family schedules and different learning preferences.
                </p>
                <Button variant="outline" className="border-secondary text-secondary-foreground hover:bg-secondary hover:text-secondary-foreground px-6 py-2">
                  Schedule a Session
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA Section */}
        <div className="hero-section bg-gradient-to-r from-primary to-primary/80 mt-16">
          <h2 className="text-4xl font-bold text-primary-foreground mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-primary-foreground/90 mb-8 max-w-3xl mx-auto">
            Contact us today to learn more about our comprehensive phonics programs and find the perfect fit for your learning needs.
          </p>
          <Button size="lg" variant="secondary" className="bg-white text-primary hover:bg-white/90 px-10 py-4 text-xl font-semibold">
            Contact Us Today
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Services;
