
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { PlayCircle, Download, BookOpen, Video, Headphones, FileText } from 'lucide-react';

const Training = () => {
  const trainingMaterials = [
    {
      title: "Introduction to Phonics/Reading and Learning Support",
      description: "Comprehensive guide to understanding the fundamentals of phonics education and learning support strategies.",
      type: "Guide",
      icon: BookOpen,
      color: "bg-blue-100 text-blue-600"
    },
    {
      title: "Practical Applications",
      description: "Hands-on activities and exercises to implement phonics teaching in real classroom settings.",
      type: "Workbook",
      icon: FileText,
      color: "bg-green-100 text-green-600"
    }
  ];

  const audioResources = [
    {
      title: "Phonics Story Creation",
      description: "Audio guide on creating engaging phonics stories for different age groups.",
      duration: "45 min",
      icon: Headphones
    },
    {
      title: "Sound and Movement",
      description: "Interactive audio sessions combining phonics with physical movement activities.",
      duration: "30 min",
      icon: Headphones
    },
    {
      title: "Reading Comprehension Techniques",
      description: "Advanced audio training on improving student reading comprehension skills.",
      duration: "60 min",
      icon: Headphones
    }
  ];

  const videoTutorials = [
    {
      title: "Reading Teaching Technique",
      description: "Step-by-step video demonstrations of effective reading teaching methods.",
      duration: "25 min",
      level: "Beginner"
    },
    {
      title: "Advanced Phonics Methods",
      description: "In-depth exploration of advanced phonics teaching strategies for challenging students.",
      duration: "40 min",
      level: "Advanced"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50">
      {/* Header Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">Training Materials</h1>
            <h2 className="text-2xl text-red-600 font-semibold mb-4">Welcome, Mrs V. Axakhoes</h2>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              Access comprehensive training resources designed to enhance your phonics teaching skills
            </p>
          </div>

          {/* Training Materials Section */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Training Materials</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {trainingMaterials.map((material, index) => {
                const IconComponent = material.icon;
                return (
                  <Card key={index} className="hover:shadow-lg transition-shadow duration-300">
                    <CardHeader>
                      <div className="flex items-center justify-between mb-4">
                        <div className={`w-12 h-12 rounded-full ${material.color} flex items-center justify-center`}>
                          <IconComponent size={24} />
                        </div>
                        <Badge variant="secondary">{material.type}</Badge>
                      </div>
                      <CardTitle className="text-xl text-gray-900">{material.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-600 mb-6">{material.description}</p>
                      <Button className="w-full bg-red-600 hover:bg-red-700 text-white">
                        <Download className="mr-2" size={16} />
                        Access Material
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* Audio Resources Section */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Audio Resources</h2>
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="space-y-6">
                {audioResources.map((resource, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="flex items-center space-x-4">
                      <div className="bg-purple-100 w-12 h-12 rounded-full flex items-center justify-center">
                        <resource.icon className="text-purple-600" size={24} />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{resource.title}</h3>
                        <p className="text-gray-600">{resource.description}</p>
                        <span className="text-sm text-gray-500">{resource.duration}</span>
                      </div>
                    </div>
                    <Button className="bg-red-600 hover:bg-red-700 text-white">
                      <PlayCircle className="mr-2" size={16} />
                      Listen
                    </Button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Video Tutorials Section */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Video Tutorials</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {videoTutorials.map((video, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow duration-300">
                  <CardHeader>
                    <div className="flex items-center justify-between mb-4">
                      <div className="bg-red-100 w-12 h-12 rounded-full flex items-center justify-center">
                        <Video className="text-red-600" size={24} />
                      </div>
                      <Badge className={video.level === 'Beginner' ? 'bg-green-500' : 'bg-orange-500'}>
                        {video.level}
                      </Badge>
                    </div>
                    <CardTitle className="text-xl text-gray-900">{video.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4">{video.description}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-500">{video.duration}</span>
                      <Button className="bg-red-600 hover:bg-red-700 text-white">
                        <PlayCircle className="mr-2" size={16} />
                        Watch
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Training;
