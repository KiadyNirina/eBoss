<script>
    import HeroSection from '../components/HeroSection.svelte';
    import FeaturesSection from '../components/FeaturesSection.svelte';
    import TestimonialsSection from '../components/TestimonialsSection.svelte';
    import PricingSection from '../components/PricingSection.svelte';
    import CtaSection from '../components/CtaSection.svelte';
    import Footer from '../components/Footer.svelte';
    import Navbar from '../components/Navbar.svelte';
</script>

<div class="min-h-screen bg-gray-50">
    <Navbar />
    
    <main>
        <HeroSection />
        <FeaturesSection />
        <!-- <TestimonialsSection />
        <PricingSection />
        <CtaSection /> -->
    </main>
    
    <Footer />
</div>