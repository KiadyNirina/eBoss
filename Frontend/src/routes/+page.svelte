<script>
    import HeroSection from '$lib/HeroSection.svelte';
    import FeaturesSection from '$lib/FeaturesSection.svelte';
    import TestimonialsSection from '$lib/TestimonialsSection.svelte';
    import PricingSection from '$lib/PricingSection.svelte';
    import CtaSection from '$lib/CtaSection.svelte';
    import Footer from '$lib/Footer.svelte';
    import Navbar from '$lib/Navbar.svelte';
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