
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Video, Headphones, FileText, Download, Play, Clock } from 'lucide-react';

const Training = () => {
  const trainingMaterials = [
    {
      title: "Introduction to Phonics/Reading and Learning Program",
      description: "Comprehensive guide to understanding the fundamentals of phonics education and effective teaching methods.",
      type: "PDF Training Guide",
      pages: "45 pages",
      icon: FileText,
      color: "primary"
    },
    {
      title: "Teaching Phonics/Reading and Learning Program",
      description: "Step-by-step instructional materials for educators to implement effective phonics teaching strategies.",
      type: "Complete Training Manual", 
      pages: "120 pages",
      icon: BookOpen,
      color: "secondary"
    }
  ];

  const audioResources = [
    {
      title: "Phonics Song Collection",
      description: "Engaging musical resources to make phonics learning fun and memorable for students.",
      type: "Audio Collection",
      duration: "45 minutes"
    },
    {
      title: "Sound Recognition Exercises", 
      description: "Audio exercises designed to improve phonetic awareness and sound recognition skills.",
      type: "Practice Audio",
      duration: "30 minutes"
    },
    {
      title: "Reading Comprehension Stories",
      description: "Narrated stories that help develop listening skills and reading comprehension abilities.",
      type: "Story Collection",
      duration: "60 minutes"
    }
  ];

  const videoTutorials = [
    {
      title: "How to Teach ABCs Effectively",
      description: "Visual demonstration of proven methods for teaching alphabet recognition and letter sounds.",
      duration: "25 minutes"
    },
    {
      title: "Interactive Learning Techniques", 
      description: "Practical examples of engaging activities that make phonics learning interactive and fun.",
      duration: "35 minutes"
    }
  ];

  return (
    <div className="page-container">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="hero-section mb-12">
          <h1 className="text-6xl md:text-7xl font-bold text-foreground mb-6">
            Training Resources
          </h1>
          <h2 className="text-3xl font-semibold text-primary mb-6">
            Welcome, Mrs V. Axakhoes
          </h2>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
            Access comprehensive training materials, resources, and tutorials to enhance your phonics teaching skills and deliver exceptional learning experiences.
          </p>
        </div>

        {/* Training Materials */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8">Core Training Materials</h2>
          <div className="space-y-6">
            {trainingMaterials.map((material, index) => (
              <Card key={index} className="bg-card border-2 border-border">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-6">
                      <div className={`p-4 rounded-full ${
                        material.color === 'primary' ? 'bg-primary/10' : 'bg-secondary/30'
                      }`}>
                        <material.icon className={`w-8 h-8 ${
                          material.color === 'primary' ? 'text-primary' : 'text-secondary-foreground'
                        }`} />
                      </div>
                      <div className="flex-1">
                        <CardTitle className="text-2xl text-foreground mb-2">{material.title}</CardTitle>
                        <div className="flex gap-4 mb-3">
                          <span className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full">{material.type}</span>
                          <span className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full">{material.pages}</span>
                        </div>
                        <p className="text-muted-foreground text-lg leading-relaxed">{material.description}</p>
                      </div>
                    </div>
                    <Button 
                      size="lg" 
                      className={`${
                        material.color === 'primary' ? 'bg-primary hover:bg-primary/90' : 'bg-secondary hover:bg-secondary/90'
                      } text-white px-6 py-3`}
                    >
                      <Download className="w-5 h-5 mr-2" />
                      Download
                    </Button>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>

        {/* Audio Resources */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8">Audio Learning Resources</h2>
          <div className="grid gap-6">
            {audioResources.map((audio, index) => (
              <Card key={index} className="bg-card border-2 border-border">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-6">
                      <div className="p-4 rounded-full bg-accent/20">
                        <Headphones className="w-8 h-8 text-accent" />
                      </div>
                      <div>
                        <CardTitle className="text-2xl text-foreground mb-2">{audio.title}</CardTitle>
                        <div className="flex gap-4 mb-3">
                          <span className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full">{audio.type}</span>
                          <span className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {audio.duration}
                          </span>
                        </div>
                        <p className="text-muted-foreground text-lg">{audio.description}</p>
                      </div>
                    </div>
                    <Button size="lg" className="bg-accent hover:bg-accent/90 text-white px-6 py-3">
                      <Play className="w-5 h-5 mr-2" />
                      Play Audio
                    </Button>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>

        {/* Video Tutorials */}
        <div className="content-section mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-8">Video Tutorial Library</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {videoTutorials.map((video, index) => (
              <Card key={index} className="bg-card border-2 border-border">
                <CardHeader>
                  <div className="flex items-center gap-4 mb-4">
                    <div className="p-3 rounded-full bg-primary/10">
                      <Video className="w-6 h-6 text-primary" />
                    </div>
                    <span className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {video.duration}
                    </span>
                  </div>
                  <CardTitle className="text-2xl text-foreground mb-3">{video.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg mb-6 leading-relaxed">{video.description}</p>
                  <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-3 text-lg">
                    <Play className="w-5 h-5 mr-2" />
                    Watch Tutorial
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Support Section */}
        <div className="hero-section bg-gradient-to-r from-secondary/20 to-accent/20">
          <h2 className="text-4xl font-bold text-foreground mb-6">
            Need Additional Support?
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Our team is here to help you make the most of these training resources. Contact us for personalized guidance and support.
          </p>
          <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-10 py-4 text-xl font-semibold">
            Get Training Support
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Training;
