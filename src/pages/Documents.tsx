
import React from 'react';
import { Download, FileText, Calendar } from 'lucide-react';

const Documents = () => {
  const documents = [
    {
      id: 1,
      title: "Party Constitution",
      description: "The founding document outlining our principles, structure, and governance framework.",
      date: "2024-01-15",
      size: "2.3 MB",
      category: "Governance"
    },
    {
      id: 2,
      title: "Economic Policy Framework",
      description: "Comprehensive policy document on economic development, job creation, and fiscal responsibility.",
      date: "2024-03-20",
      size: "4.1 MB",
      category: "Policy"
    },
    {
      id: 3,
      title: "Education Reform Proposal",
      description: "Detailed plan for improving Namibia's education system from primary to tertiary level.",
      date: "2024-04-10",
      size: "3.7 MB",
      category: "Policy"
    },
    {
      id: 4,
      title: "Healthcare Accessibility Plan",
      description: "Strategy for expanding healthcare access and improving medical services nationwide.",
      date: "2024-05-05",
      size: "2.8 MB",
      category: "Policy"
    },
    {
      id: 5,
      title: "Environmental Protection Charter",
      description: "Our commitment to environmental conservation and sustainable development practices.",
      date: "2024-05-25",
      size: "1.9 MB",
      category: "Environment"
    },
    {
      id: 6,
      title: "Youth Empowerment Strategy",
      description: "Comprehensive approach to creating opportunities and supporting young Namibians.",
      date: "2024-06-10",
      size: "3.2 MB",
      category: "Youth"
    }
  ];

  const categories = [...new Set(documents.map(doc => doc.category))];

  const handleDownload = (documentId: number, title: string) => {
    // In a real application, this would trigger the actual download
    console.log(`Downloading document: ${title}`);
    // You would typically make an API call here to get the actual file
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold text-center mb-4">
            Party Documents
          </h1>
          <p className="text-xl text-center max-w-3xl mx-auto">
            Access our official documents, policy papers, and public statements
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="mb-8">
          <div className="flex flex-wrap gap-2 justify-center">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
              All Documents
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

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {documents.map(document => (
            <div key={document.id} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow duration-200">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <FileText className="text-blue-600 mr-2" size={24} />
                  <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    {document.category}
                  </span>
                </div>
                <span className="text-gray-500 text-sm">{document.size}</span>
              </div>
              
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {document.title}
              </h3>
              
              <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                {document.description}
              </p>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center text-gray-500 text-sm">
                  <Calendar size={16} className="mr-1" />
                  {new Date(document.date).toLocaleDateString()}
                </div>
                
                <button
                  onClick={() => handleDownload(document.id, document.title)}
                  className="flex items-center bg-blue-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors duration-200"
                >
                  <Download size={16} className="mr-1" />
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-white rounded-lg shadow-lg p-8 text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Document Request
          </h3>
          <p className="text-gray-600 mb-6">
            Can't find the document you're looking for? Contact us to request access to additional party materials.
          </p>
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200">
            Request Document
          </button>
        </div>
      </div>
    </div>
  );
};

export default Documents;
