<script>
  import Icon from '@iconify/svelte';
  
  const testimonials = [
    {
      name: 'Marie Dupont',
      role: 'Directrice, Lycée Saint-Exupéry',
      content: 'EduManage a transformé notre façon de gérer l\'établissement. Tout est maintenant centralisé et accessible en quelques clics.',
      avatar: '/avatars/marie-dupont.jpg'
    },
    {
      name: 'Jean Martin',
      role: 'Proviseur, Collège Voltaire',
      content: 'La gestion des emplois du temps était un cauchemar avant EduManage. Maintenant, c\'est un jeu d\'enfant et les enseignants sont ravis.',
      avatar: '/avatars/jean-martin.jpg'
    },
    {
      name: 'Sophie Lambert',
      role: 'Secrétaire, École Primaire Les Lilas',
      content: 'Les parents apprécient particulièrement le module de communication et la transparence sur les notes et les absences.',
      avatar: '/avatars/sophie-lambert.jpg'
    }
  ];
</script>

<section id="testimonials" class="py-12 bg-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="lg:text-center">
      <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Témoignages</h2>
      <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
        Ils utilisent déjà EduManage
      </p>
    </div>

    <div class="mt-10 grid grid-cols-1 gap-10 md:grid-cols-3">
      {#each testimonials as testimonial}
        <div class="bg-gray-50 p-8 rounded-lg shadow-sm">
          <div class="flex items-center">
            <!-- <img class="h-12 w-12 rounded-full" src={testimonial.avatar} alt={testimonial.name} /> -->
            <div class="ml-4">
              <div class="text-lg font-medium text-gray-900">{testimonial.name}</div>
              <div class="text-indigo-600">{testimonial.role}</div>
            </div>
          </div>
          <div class="mt-6">
            <Icon icon="heroicons:quote" class="h-6 w-6 text-gray-400" />
            <p class="mt-2 text-gray-600">
              "{testimonial.content}"
            </p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>