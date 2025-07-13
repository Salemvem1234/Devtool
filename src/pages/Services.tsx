
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Users, GraduationCap, Star, Clock, Heart } from 'lucide-react';

const Services = () => {
  const services = [
    {
      title: "Early Learners (Ages 4-6)",
      description: "Foundation phonics program designed for young children just starting their reading journey. Interactive games and activities make learning fun and engaging.",
      features: ["Letter recognition", "Sound blending", "Simple word formation", "Visual and auditory learning"],
      icon: Heart,
      color: "primary"
    },
    {
      title: "Primary School (Ages 7-10)",
      description: "Advanced phonics and spelling program that builds on foundation skills with more complex reading and writing activities.",
      features: ["Complex phonics patterns", "Spelling rules", "Reading comprehension", "Writing skills"],
      icon: BookOpen,
      color: "secondary"
    },
    {
      title: "Teenagers (Ages 11-14)",
      description: "Specialized program for older students who need additional support with reading and spelling skills.",
      features: ["Literacy development", "Study skills", "Confidence building", "Exam preparation"],
      icon: GraduationCap,
      color: "accent"
    }
  ];

  return (
    <div className="page-container">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="rounded-section text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Services
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We offer comprehensive phonics education programs tailored for different age groups and learning needs. 
            Our structured approach ensures effective learning outcomes for every student.
          </p>
        </div>

        {/* Services Grid */}
        <div className="space-y-6">
          {services.map((service, index) => (
            <div key={index} className="rounded-section">
              <Card className="bg-card/50 border-2 border-border">
                <CardHeader>
                  <div className="flex items-center gap-4 mb-4">
                    <div className={`p-3 rounded-full ${
                      service.color === 'primary' ? 'bg-primary/10' :
                      service.color === 'secondary' ? 'bg-secondary/30' :
                      'bg-accent/20'
                    }`}>
                      <service.icon className={`w-8 h-8 ${
                        service.color === 'primary' ? 'text-primary' :
                        service.color === 'secondary' ? 'text-secondary-foreground' :
                        'text-accent'
                      }`} />
                    </div>
                    <div>
                      <CardTitle className="text-2xl text-foreground">{service.title}</CardTitle>
                    </div>
                  </div>
                  <p className="text-muted-foreground">{service.description}</p>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4 mb-6">
                    {service.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center gap-2">
                        <Star className="w-4 h-4 text-secondary" />
                        <span className="text-foreground">{feature}</span>
                      </div>
                    ))}
                  </div>
                  <Button 
                    className={`w-full md:w-auto ${
                      service.color === 'primary' ? 'bg-primary hover:bg-primary/90' :
                      service.color === 'secondary' ? 'bg-secondary hover:bg-secondary/90' :
                      'bg-accent hover:bg-accent/90'
                    } text-white`}
                  >
                    Learn More
                  </Button>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>

        {/* Additional Services */}
        <div className="rounded-section mt-8">
          <h2 className="text-3xl font-bold text-foreground mb-6 text-center">Additional Services</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="bg-card/50 border-2 border-border">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Users className="w-6 h-6 text-primary" />
                  <CardTitle className="text-xl">Group Classes</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  Small group sessions that encourage peer learning and social interaction while maintaining personalized attention.
                </p>
                <Button variant="outline" className="border-primary text-primary hover:bg-primary hover:text-primary-foreground">
                  Join a Group
                </Button>
              </CardContent>
            </Card>

            <Card className="bg-card/50 border-2 border-border">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Clock className="w-6 h-6 text-secondary" />
                  <CardTitle className="text-xl">Flexible Scheduling</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  We offer flexible scheduling options to accommodate busy family schedules and different learning preferences.
                </p>
                <Button variant="outline" className="border-secondary text-secondary-foreground hover:bg-secondary hover:text-secondary-foreground">
                  Schedule Now
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA Section */}
        <div className="rounded-section bg-primary text-center mt-8">
          <h2 className="text-3xl font-bold text-primary-foreground mb-4">
            Subscribe Now
          </h2>
          <p className="text-primary-foreground/90 mb-6">
            Get started with our comprehensive phonics programs today!
          </p>
          <Button size="lg" variant="secondary" className="bg-card text-foreground hover:bg-card/90 px-8 py-3">
            Subscribe Now
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Services;
