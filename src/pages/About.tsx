
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { User, Award, BookOpen, Heart, GraduationCap, Star } from 'lucide-react';

const About = () => {
  return (
    <div className="page-container">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="hero-section mb-12">
          <h1 className="text-6xl md:text-7xl font-bold text-foreground mb-6">
            About Us
          </h1>
          <h2 className="text-3xl font-semibold text-primary mb-6">
            Meet Veronica Axakhoes
          </h2>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
            Discover the passion and expertise behind Axaphonics - where quality phonics education meets innovative teaching methods.
          </p>
        </div>

        {/* Main About Section */}
        <div className="content-section mb-12">
          <div className="grid md:grid-cols-3 gap-12">
            <div className="md:col-span-1 flex justify-center">
              <div className="w-64 h-64 bg-gradient-to-br from-primary/10 to-secondary/20 rounded-full flex items-center justify-center border-4 border-primary/20 shadow-2xl">
                <User size={120} className="text-primary" />
              </div>
            </div>
            
            <div className="md:col-span-2">
              <Card className="bg-card border-2 border-border h-full">
                <CardHeader>
                  <CardTitle className="text-3xl text-foreground flex items-center gap-4">
                    <Award className="w-8 h-8 text-secondary" />
                    Mrs. Veronica Axakhoes
                  </CardTitle>
                  <p className="text-xl text-primary font-bold">Founder & Lead Educator</p>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg mb-6 leading-relaxed">
                    With over 15 years of experience in phonics education, Mrs. Veronica Axakhoes has dedicated her career to helping students of all ages develop strong reading foundations. Her passion for education and innovative teaching methods have transformed countless lives.
                  </p>
                  <p className="text-muted-foreground text-lg leading-relaxed">
                    She holds advanced certifications in phonics instruction and has developed unique methodologies that make learning both effective and enjoyable for students from early childhood through teenage years.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* Philosophy Section */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8 text-center">Teaching Philosophy</h2>
          <Card className="bg-gradient-to-br from-card to-muted/50 border-2 border-border">
            <CardContent className="pt-8">
              <blockquote className="text-2xl text-muted-foreground font-medium leading-relaxed mb-8 text-center italic">
                "Every child deserves to experience the joy of reading. My approach combines proven phonics methods with creative, engaging activities that make learning natural and fun. I believe that with the right foundation, every student can become a confident reader."
              </blockquote>
              <div className="grid md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Heart className="w-10 h-10 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold text-foreground mb-3">Personalized Care</h3>
                  <p className="text-muted-foreground leading-relaxed">Individual attention for every student's unique learning style and pace</p>
                </div>
                <div className="text-center">
                  <div className="w-20 h-20 bg-secondary/30 rounded-full flex items-center justify-center mx-auto mb-4">
                    <BookOpen className="w-10 h-10 text-secondary-foreground" />
                  </div>
                  <h3 className="text-xl font-bold text-foreground mb-3">Proven Methods</h3>
                  <p className="text-muted-foreground leading-relaxed">Research-based techniques that deliver consistent and measurable results</p>
                </div>
                <div className="text-center">
                  <div className="w-20 h-20 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Award className="w-10 h-10 text-accent" />
                  </div>
                  <h3 className="text-xl font-bold text-foreground mb-3">Excellence</h3>
                  <p className="text-muted-foreground leading-relaxed">Unwavering commitment to the highest standards of education</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Mission Statement */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8 text-center">Our Mission</h2>
          <Card className="bg-gradient-to-r from-primary to-primary/80 text-center border-2 border-primary">
            <CardContent className="pt-12 pb-12">
              <p className="text-xl text-primary-foreground leading-relaxed mb-8 max-w-4xl mx-auto">
                "To provide exceptional phonics education that builds confident, capable readers and lifelong learners. 
                We are committed to making reading accessible, enjoyable, and successful for students of all ages and abilities 
                through innovative teaching methods and personalized instruction."
              </p>
              <Button size="lg" variant="secondary" className="bg-white text-primary hover:bg-white/90 px-10 py-4 text-xl font-semibold">
                Join Our Learning Community
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Qualifications */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8">Professional Qualifications & Experience</h2>
          <Card className="bg-card border-2 border-border">
            <CardContent className="pt-8">
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-3 h-3 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">Master's Degree in Education</h3>
                    <p className="text-muted-foreground text-lg">Specialization in Reading and Literacy with advanced research in phonics instruction</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-3 h-3 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">Certified Phonics Instructor</h3>
                    <p className="text-muted-foreground text-lg">Advanced training credentials with ongoing professional development</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-3 h-3 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">15+ Years Teaching Experience</h3>
                    <p className="text-muted-foreground text-lg">Hands-on teaching experience across all age groups from early learners to teens</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-3 h-3 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">Curriculum Developer</h3>
                    <p className="text-muted-foreground text-lg">Creator of innovative phonics curricula and teaching methodologies</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-3 h-3 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">Award-Winning Educator</h3>
                    <p className="text-muted-foreground text-lg">Recognized educator with multiple awards for excellence in literacy instruction</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Success Stories */}
        <div className="hero-section bg-gradient-to-br from-secondary/20 to-accent/20">
          <h2 className="text-4xl font-bold text-foreground mb-6">
            Transforming Lives Through Reading
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-4xl mx-auto">
            Over the years, we've helped thousands of students discover the joy of reading and build the confidence they need to succeed in their educational journey.
          </p>
          <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-10 py-4 text-xl font-semibold">
            Start Your Learning Journey
          </Button>
        </div>
      </div>
    </div>
  );
};

export default About;
