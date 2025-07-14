
const Footer = () => {
  return (
    <footer className="nav-gradient py-12 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Brand Section */}
          <div className="text-center md:text-left">
            <h3 className="text-3xl font-bold text-white mb-3">Axaphonics</h3>
            <p className="text-white/90 text-lg mb-4">Learn Phonics the Fun Way!</p>
            <p className="text-white/80">
              Building strong reading foundations through engaging and effective phonics education.
            </p>
          </div>
          
          {/* Contact Info */}
          <div className="text-center">
            <h4 className="text-xl font-semibold text-white mb-4">Get In Touch</h4>
            <div className="space-y-2 text-white/90">
              <p>axaphonics@gmail.com</p>
              <p>+27 (0) 11 234 5678</p>
              <p>axaphonics.co.za</p>
            </div>
          </div>
          
          {/* Social Links */}
          <div className="text-center md:text-right">
            <h4 className="text-xl font-semibold text-white mb-4">Follow Us</h4>
            <div className="space-y-2 text-white/90">
              <p>facebook.com/axaphonics</p>
              <p>instagram.com/axaphonics</p>
            </div>
          </div>
        </div>
        
        <div className="border-t border-white/20 mt-8 pt-8 text-center">
          <p className="text-white/80">
            © 2024 Axaphonics. All rights reserved. | Privacy Policy | Terms of Service
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
