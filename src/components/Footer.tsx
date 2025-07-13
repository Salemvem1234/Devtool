
const Footer = () => {
  return (
    <footer className="bg-secondary py-8 mt-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="text-center md:text-left mb-4 md:mb-0">
            <h3 className="text-2xl font-bold text-secondary-foreground">Axaphonics</h3>
            <p className="text-secondary-foreground/80 mt-1">Learn Phonics the Fun Way!</p>
          </div>
          
          <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6">
            <p className="text-secondary-foreground/80 text-sm">
              © 2024 Axaphonics. All rights reserved.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-secondary-foreground/80 hover:text-secondary-foreground transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-secondary-foreground/80 hover:text-secondary-foreground transition-colors">
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
