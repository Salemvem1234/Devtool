
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { User, Award, BookOpen, Heart } from 'lucide-react';

const About = () => {
  return (
    <div className="page-container">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="rounded-section text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            About
          </h1>
          <h2 className="text-2xl font-semibold text-primary mb-4">
            About Veronica Axakhoes
          </h2>
        </div>

        {/* Main About Section */}
        <div className="rounded-section mb-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-1 flex justify-center">
              <div className="w-48 h-48 bg-primary/10 rounded-full flex items-center justify-center border-4 border-primary/20">
                <User size={80} className="text-primary" />
              </div>
            </div>
            
            <div className="md:col-span-2">
              <Card className="bg-card/50 border-2 border-border h-full">
                <CardHeader>
                  <CardTitle className="text-2xl text-foreground flex items-center gap-3">
                    <Award className="w-6 h-6 text-secondary" />
                    Mrs. V. Axakhoes
                  </CardTitle>
                  <p className="text-lg text-primary font-semibold">Founder & Lead Educator</p>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4 leading-relaxed">
                    With over 15 years of experience in phonics education, Mrs. Veronica Axakhoes has dedicated her career to helping students of all ages develop strong reading foundations. Her passion for education and innovative teaching methods have transformed countless lives.
                  </p>
                  <p className="text-muted-foreground leading-relaxed">
                    She holds advanced certifications in phonics instruction and has developed unique methodologies that make learning both effective and enjoyable for students from early childhood through teenage years.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* Veronica's Approach */}
        <div className="rounded-section mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-6 text-center">Veronica's Approach</h2>
          <Card className="bg-card/50 border-2 border-border">
            <CardContent className="pt-6">
              <p className="text-muted-foreground text-lg leading-relaxed mb-6">
                "Every child deserves to experience the joy of reading. My approach combines proven phonics methods with creative, engaging activities that make learning natural and fun. I believe that with the right foundation, every student can become a confident reader."
              </p>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Heart className="w-8 h-8 text-primary" />
                  </div>
                  <h3 className="font-semibold text-foreground mb-2">Personalized Care</h3>
                  <p className="text-sm text-muted-foreground">Individual attention for every student's unique learning style</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-secondary/30 rounded-full flex items-center justify-center mx-auto mb-3">
                    <BookOpen className="w-8 h-8 text-secondary-foreground" />
                  </div>
                  <h3 className="font-semibold text-foreground mb-2">Proven Methods</h3>
                  <p className="text-sm text-muted-foreground">Research-based techniques that deliver consistent results</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Award className="w-8 h-8 text-accent" />
                  </div>
                  <h3 className="font-semibold text-foreground mb-2">Excellence</h3>
                  <p className="text-sm text-muted-foreground">Commitment to the highest standards of education</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Mission Statement */}
        <div className="rounded-section mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-6 text-center">Our Mission</h2>
          <Card className="bg-primary text-center border-2 border-primary">
            <CardContent className="pt-8 pb-8">
              <p className="text-primary-foreground text-lg leading-relaxed mb-4">
                "To provide exceptional phonics education that builds confident, capable readers and lifelong learners. 
                We are committed to making reading accessible, enjoyable, and successful for students of all ages and abilities."
              </p>
              <Button variant="secondary" size="lg" className="bg-card text-foreground hover:bg-card/90">
                Join Our Community
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Qualifications */}
        <div className="rounded-section">
          <h2 className="text-3xl font-bold text-foreground mb-6">Qualifications & Experience</h2>
          <div className="space-y-4">
            <Card className="bg-card/50 border-2 border-border">
              <CardContent className="pt-4">
                <ul className="space-y-3 text-muted-foreground">
                  <li className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <span>Master's Degree in Education with specialization in Reading and Literacy</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <span>Certified Phonics Instructor with advanced training credentials</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <span>15+ years of hands-on teaching experience across all age groups</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <span>Developer of innovative phonics curricula and teaching methodologies</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <span>Recognized educator with awards for excellence in literacy instruction</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
