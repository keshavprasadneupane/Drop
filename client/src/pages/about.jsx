import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import Nischal from "../assets/images/nischalBabu.jpg"
import Keshav from "../assets/images/keshavBabu.jpg"

const About = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar bgstate={true} />

      <main className="flex-1 w-full pt-20 sm:pt-24">
        {/* Editorial Hero Header */}
        <section className="relative w-full py-20 sm:py-28 lg:py-32 bg-neutral-900 text-white overflow-hidden">
          <div
            className="absolute inset-0 bg-cover bg-center opacity-30 mix-blend-luminosity"
            style={{
              backgroundImage:
                "url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=1600&auto=format&fit=crop')",
            }}
          />
          <div className="relative max-w-4xl mx-auto px-4 sm:px-6 text-center flex flex-col items-center">
            <span className="text-xs uppercase tracking-widest text-neutral-400 font-medium mb-3">
              Established 2026
            </span>
            <h1 className="font-medium text-3xl sm:text-5xl lg:text-6xl tracking-tight leading-tight mb-6">
              Essential Aesthetics. Crafted For Everyday Living.
            </h1>
            <p className="font-light text-neutral-300 text-base sm:text-lg leading-relaxed max-w-2xl">
              DROPP was conceived with a singular ambition: strip away seasonal
              noise to create heavyweight, impeccably tailored garments that
              outlive trends.
            </p>
          </div>
        </section>

        {/* The Brand Narrative */}
        <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            <div className="flex flex-col gap-6">
              <span className="text-xs uppercase tracking-widest text-neutral-400 font-semibold">
                Our Story
              </span>
              <h2 className="font-medium text-2xl sm:text-3xl lg:text-4xl text-neutral-900 leading-snug">
                We believe what you wear should speak quietly, with exceptional
                form and substance.
              </h2>
              <div className="space-y-4 text-sm sm:text-base text-neutral-600 font-light leading-relaxed">
                <p>
                  Founded in response to disposable fast fashion, DROPP is a
                  design studio exploring modern silhouettes, relaxed
                  proportions, and premium tactile materials.
                </p>
                <p>
                  Every drop is developed through meticulous prototyping:
                  calibrating shoulder drops, selecting ring-spun combed cotton
                  weights from 240gsm to 450gsm, and curating restrained neutral
                  color palettes that seamlessly integrate into your rotation.
                </p>
              </div>
            </div>

            <div className="relative aspect-4/5 w-full overflow-hidden bg-neutral-100 rounded-xs shadow-md">
              <img
                src="https://images.unsplash.com/photo-1558769132-cb1aea458c5e?q=80&w=1200&auto=format&fit=crop"
                alt="DROPP Studio & Workshop"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </section>

        {/* 3 Core Pillars */}
        <section className="bg-neutral-50 py-16 sm:py-24 border-y border-black/10">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-xl mx-auto mb-14">
              <span className="text-xs uppercase tracking-widest text-neutral-400 font-semibold">
                Commitments
              </span>
              <h2 className="font-medium text-2xl sm:text-3xl text-neutral-900 mt-2">
                The DROPP Standards
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-10">
              <div className="flex flex-col p-6 sm:p-8 bg-white border border-black/5 hover:border-black/20 transition-all">
                <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center text-xl mb-6">
                  🧵
                </div>
                <h3 className="font-medium text-lg text-neutral-900 mb-2">
                  Heavyweight Fabrics
                </h3>
                <p className="text-sm text-neutral-600 font-light leading-relaxed">
                  We use bespoke 100% certified combed cotton, heavyweight
                  loopback French terry, and durable denim weaves that soften
                  with age instead of wearing down.
                </p>
              </div>

              <div className="flex flex-col p-6 sm:p-8 bg-white border border-black/5 hover:border-black/20 transition-all">
                <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center text-xl mb-6">
                  📐
                </div>
                <h3 className="font-medium text-lg text-neutral-900 mb-2">
                  Architectural Cuts
                </h3>
                <p className="text-sm text-neutral-600 font-light leading-relaxed">
                  Relaxed drape meets structured lines. Our garments are cut
                  with precision to ensure an effortless profile that works
                  universally.
                </p>
              </div>

              <div className="flex flex-col p-6 sm:p-8 bg-white border border-black/5 hover:border-black/20 transition-all">
                <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center text-xl mb-6">
                  🌱
                </div>
                <h3 className="font-medium text-lg text-neutral-900 mb-2">
                  Responsible Production
                </h3>
                <p className="text-sm text-neutral-600 font-light leading-relaxed">
                  Small-batch manufacturing ensures near-zero deadstock waste.
                  We partner only with verified facilities that treat workers
                  with dignity.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Meet The Makers */}
        <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-12">
            <div>
              <span className="text-xs uppercase tracking-widest text-neutral-400 font-semibold">
                Behind the Scenes
              </span>
              <h2 className="font-medium text-2xl sm:text-3xl text-neutral-900 mt-2">
                Meet the Makers
              </h2>
            </div>
            <p className="text-sm text-neutral-500 font-light max-w-md">
              From patternmakers to textile dyers, each garment passes through
              skilled hands dedicated to sartorial excellence.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 max-w-2xl mx-auto">
            <div className="flex flex-col">
              <div className="aspect-3/4 bg-neutral-100 overflow-hidden mb-3">
                <img
                  src={Nischal}
                  alt="Nischal Pokharel"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="font-medium text-base text-neutral-900">
                Nischal Pokharel
              </h3>
              <span className="text-xs text-neutral-500">
                Frontend Developer
              </span>
            </div>

            <div className="flex flex-col">
              <div className="aspect-3/4 bg-neutral-100 overflow-hidden mb-3">
                <img
                  src={Keshav}
                  alt="Aria Chen"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="font-medium text-base text-neutral-900">
                Keshav Prasad Neupane
              </h3>
              <span className="text-xs text-neutral-500">
                Backend Developer
              </span>
            </div>
          </div>
        </section>

        {/* CTA Footer Banner */}
        <section className="bg-black text-white py-16 px-4 sm:px-6 text-center">
          <div className="max-w-2xl mx-auto flex flex-col items-center gap-6">
            <h2 className="font-medium text-2xl sm:text-4xl">
              Experience the New Standard
            </h2>
            <p className="text-neutral-400 font-light text-sm sm:text-base">
              Discover our latest drop and build a cohesive, long-lasting
              wardrobe today.
            </p>
            <button
              onClick={() => navigate("/collection")}
              className="bg-white text-black px-8 py-3.5 text-sm font-medium hover:bg-neutral-200 transition-all cursor-pointer"
            >
              Shop All Collections
            </button>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default About;
