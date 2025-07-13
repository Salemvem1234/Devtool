
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Video, Headphones, FileText, Download, Play } from 'lucide-react';

const Training = () => {
  const trainingMaterials = [
    {
      title: "Introduction to Phonics/Reading and Learning Program",
      description: "Comprehensive guide to understanding the fundamentals of phonics education and effective teaching methods.",
      type: "PDF Guide",
      icon: FileText,
      color: "primary"
    },
    {
      title: "Teaching Phonics/Reading and Learning Program",
      description: "Step-by-step instructional materials for educators to implement effective phonics teaching strategies.",
      type: "Training Manual",
      icon: BookOpen,
      color: "secondary"
    }
  ];

  const audioResources = [
    {
      title: "Phonics Song Collection",
      description: "Engaging musical resources to make phonics learning fun and memorable for students.",
      type: "Audio Collection",
      duration: "45 mins"
    },
    {
      title: "Sound Recognition Exercises",
      description: "Audio exercises designed to improve phonetic awareness and sound recognition skills.",
      type: "Exercise Audio",
      duration: "30 mins"
    },
    {
      title: "Reading Comprehension Stories",
      description: "Narrated stories that help develop listening skills and reading comprehension abilities.",
      type: "Story Audio",
      duration: "1 hour"
    }
  ];

  const videoTutorials = [
    {
      title: "How to Teach ABCs Effectively",
      description: "Visual demonstration of proven methods for teaching alphabet recognition and letter sounds.",
      duration: "25 mins"
    },
    {
      title: "Interactive Learning Techniques",
      description: "Practical examples of engaging activities that make phonics learning interactive and fun.",
      duration: "35 mins"
    }
  ];

  return (
    <div className="page-container">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="rounded-section text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Training
          </h1>
          <h2 className="text-2xl font-semibold text-primary mb-4">
            Welcome, Mrs V. Axakhoes
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Access comprehensive training materials, resources, and tutorials to enhance your phonics teaching skills.
          </p>
        </div>

        {/* Training Materials */}
        <div className="rounded-section mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-6">Training Materials</h2>
          <div className="space-y-4">
            {trainingMaterials.map((material, index) => (
              <Card key={index} className="bg-card/50 border-2 border-border">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`p-3 rounded-full ${
                        material.color === 'primary' ? 'bg-primary/10' : 'bg-secondary/30'
                      }`}>
                        <material.icon className={`w-6 h-6 ${
                          material.color === 'primary' ? 'text-primary' : 'text-secondary-foreground'
                        }`} />
                      </div>
                      <div>
                        <CardTitle className="text-xl text-foreground">{material.title}</CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">{material.type}</p>
                      </div>
                    </div>
                    <Button 
                      size="sm" 
                      className={`${
                        material.color === 'primary' ? 'bg-primary hover:bg-primary/90' : 'bg-secondary hover:bg-secondary/90'
                      } text-white`}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{material.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Audio Resources */}
        <div className="rounded-section mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-6">Audio Resources</h2>
          <div className="space-y-4">
            {audioResources.map((audio, index) => (
              <Card key={index} className="bg-card/50 border-2 border-border">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="p-3 rounded-full bg-accent/20">
                        <Headphones className="w-6 h-6 text-accent" />
                      </div>
                      <div>
                        <CardTitle className="text-lg text-foreground">{audio.title}</CardTitle>
                        <p className="text-sm text-muted-foreground">{audio.type} • {audio.duration}</p>
                      </div>
                    </div>
                    <Button size="sm" className="bg-accent hover:bg-accent/90 text-white">
                      <Play className="w-4 h-4 mr-2" />
                      Play
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{audio.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Video Tutorials */}
        <div className="rounded-section mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-6">Video Tutorials</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {videoTutorials.map((video, index) => (
              <Card key={index} className="bg-card/50 border-2 border-border">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 rounded-full bg-primary/10">
                      <Video className="w-5 h-5 text-primary" />
                    </div>
                    <span className="text-sm text-muted-foreground">{video.duration}</span>
                  </div>
                  <CardTitle className="text-lg text-foreground">{video.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">{video.description}</p>
                  <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
                    <Play className="w-4 h-4 mr-2" />
                    Watch Now
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Training;
