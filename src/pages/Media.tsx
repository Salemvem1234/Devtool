
import React from 'react';
import { Calendar, ArrowRight, Tag } from 'lucide-react';

const Media = () => {
  const mediaArticles = [
    {
      id: 1,
      title: "People Unite for Change Launches Community Outreach Program",
      excerpt: "Our party announces new initiatives to engage directly with communities across Namibia, focusing on grassroots democracy and citizen participation in the political process.",
      content: "In a groundbreaking move to strengthen democratic participation, People Unite for Change has launched a comprehensive community outreach program across all 14 regions of Namibia...",
      date: "2024-06-20",
      category: "Community",
      author: "Communications Team",
      featured: true
    },
    {
      id: 2,
      title: "Economic Policy Framework Released for Public Review",
      excerpt: "Comprehensive economic policy document outlines our vision for sustainable growth, job creation, and poverty reduction strategies for Namibia's future.",
      content: "The detailed economic framework addresses key challenges facing Namibia, including unemployment, income inequality, and sustainable development goals...",
      date: "2024-06-18",
      category: "Policy",
      author: "Policy Research Team",
      featured: true
    },
    {
      id: 3,
      title: "Youth Leadership Summit Scheduled for July 2024",
      excerpt: "Young leaders from across the country will gather to discuss the future of Namibian politics and their role in shaping democratic change.",
      content: "The summit will bring together 200 young leaders aged 18-35 from all regions to participate in workshops, panel discussions, and policy development sessions...",
      date: "2024-06-15",
      category: "Youth",
      author: "Youth Development Committee",
      featured: false
    },
    {
      id: 4,
      title: "Environmental Conservation Initiative Launched",
      excerpt: "New program focuses on protecting Namibia's natural heritage while promoting sustainable economic development across rural communities.",
      content: "The initiative includes tree planting campaigns, water conservation projects, and sustainable agriculture training programs...",
      date: "2024-06-12",
      category: "Environment",
      author: "Environmental Policy Team",
      featured: false
    },
    {
      id: 5,
      title: "Education Reform Proposal Gains Public Support",
      excerpt: "Public consultations reveal strong support for proposed changes to Namibia's education system, focusing on improved access and quality.",
      content: "Following extensive public consultations across all regions, the education reform proposal has received overwhelming support from parents, teachers, and students...",
      date: "2024-06-08",
      category: "Education",
      author: "Education Policy Committee",
      featured: false
    },
    {
      id: 6,
      title: "Healthcare Accessibility Plan Unveiled",
      excerpt: "Comprehensive strategy to improve healthcare delivery and accessibility in both urban and rural areas of Namibia.",
      content: "The plan includes mobile health clinics, telemedicine programs, and increased investment in healthcare infrastructure...",
      date: "2024-06-05",
      category: "Healthcare",
      author: "Healthcare Policy Team",
      featured: false
    }
  ];

  const categories = [...new Set(mediaArticles.map(article => article.category))];
  const featuredArticles = mediaArticles.filter(article => article.featured);
  const regularArticles = mediaArticles.filter(article => !article.featured);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold text-center mb-4">
            Media & News
          </h1>
          <p className="text-xl text-center max-w-3xl mx-auto">
            Stay updated with our latest news, press releases, and media coverage
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Filter Categories */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2 justify-center">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
              All News
            </button>
            {categories.map(category => (
              <button 
                key={category}
                className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-300 transition-colors"
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Featured Articles */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Stories</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {featuredArticles.map(article => (
              <div key={article.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-200">
                <div className="h-48 bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
                  <span className="text-white text-lg font-bold">Featured Story</span>
                </div>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <Tag size={16} className="text-blue-600 mr-1" />
                      <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                        {article.category}
                      </span>
                    </div>
                    <div className="flex items-center text-gray-500 text-sm">
                      <Calendar size={16} className="mr-1" />
                      {new Date(article.date).toLocaleDateString()}
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-3">
                    {article.title}
                  </h3>
                  
                  <p className="text-gray-600 mb-4">
                    {article.excerpt}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">By {article.author}</span>
                    <button className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium">
                      Read More
                      <ArrowRight size={16} className="ml-1" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Regular Articles */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Latest News</h2>
          <div className="space-y-6">
            {regularArticles.map(article => (
              <div key={article.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
                <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
                  <div className="flex items-center mb-2 md:mb-0">
                    <Tag size={16} className="text-blue-600 mr-1" />
                    <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded mr-4">
                      {article.category}
                    </span>
                    <span className="text-sm text-gray-500">By {article.author}</span>
                  </div>
                  <div className="flex items-center text-gray-500 text-sm">
                    <Calendar size={16} className="mr-1" />
                    {new Date(article.date).toLocaleDateString()}
                  </div>
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {article.title}
                </h3>
                
                <p className="text-gray-600 mb-4">
                  {article.excerpt}
                </p>
                
                <button className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium">
                  Read Full Article
                  <ArrowRight size={16} className="ml-1" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Media Contact Section */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-8 text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Media Inquiries
          </h3>
          <p className="text-gray-600 mb-6">
            For press releases, interviews, or media-related questions, please contact our communications team.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200">
              Contact Media Team
            </button>
            <button className="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-blue-50 transition-colors duration-200">
              Download Press Kit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Media;
