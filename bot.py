import asyncio
import logging
import random
import math
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold

from flask import Flask, request, jsonify
import nest_asyncio  # ИСПРАВЛЕНО

nest_asyncio.apply()
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = "8380435343:AAHPJhs82nxWUUxBul3jfPtiVh908n8RrIg"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Классы состояний
class TaskStates(StatesGroup):
    viewing_task = State()

# Разделы физики
SECTIONS = {
    "mechanics": "📐 Механика",
    "thermodynamics": "🔥 Термодинамика",
    "electrodynamics": "⚡ Электродинамика",
    "optics": "🔦 Оптика",
    "quantum": "⚛️ Квантовая физика"
}

# Класс генератора задач
class TaskGenerator:
    def __init__(self):
        # Словарь с генераторами задач по разделам
        self.generators = {
            "mechanics": [
                self.mech_uniform_motion,
                self.mech_accelerated_motion,
                self.mech_second_law,
                self.mech_inclined_plane,
                self.mech_projectile_motion,
                self.mech_collision,
                self.mech_energy,
                self.mech_circular_motion,
                self.mech_pendulum,
                self.mech_lever,
                self.mech_pressure,
                self.mech_springs
            ],
            "thermodynamics": [
                self.thermo_ideal_gas,
                self.thermo_isobaric,
                self.thermo_heat_capacity,
                self.thermo_first_law,
                self.thermo_carnot,
                self.thermo_phase_change,
                self.thermo_work,
                self.thermo_adiabatic,
                self.thermo_isochoric,
                self.thermo_humidity,
                self.thermo_mixture,
                self.thermo_dalton
            ],
            "electrodynamics": [
                self.electro_coulomb,
                self.electro_field,
                self.electro_ohm,
                self.electro_power,
                self.electro_series,
                self.electro_parallel,
                self.electro_work,
                self.electro_capacitor,
                self.electro_ampere,
                self.electro_induction,
                self.electro_magnetic_field,
                self.electro_joule
            ],
            "optics": [
                self.optics_reflection,
                self.optics_refraction,
                self.optics_lens,
                self.optics_magnification,
                self.optics_mirror,
                self.optics_interference,
                self.optics_power,
                self.optics_total_reflection,
                self.optics_wave,
                self.optics_polarization,
                self.optics_dispersion,
                self.optics_fiber
            ],
            "quantum": [
                self.quantum_photoeffect,
                self.quantum_spectrum,
                self.quantum_bohr,
                self.quantum_debroglie,
                self.quantum_photon,
                self.quantum_uncertainty,
                self.quantum_decay,
                self.quantum_mass_defect,
                self.quantum_compton,
                self.quantum_alpha,
                self.quantum_dual,
                self.quantum_wien
            ]
        }
    
    # ============= МЕХАНИКА =============
    
    def mech_uniform_motion(self):
        """Равномерное движение"""
        v = random.randint(10, 60)
        t = random.randint(5, 30)
        s = v * t
        
        task = f"🚂 Поезд движется равномерно со скоростью {v} м/с. Какое расстояние он пройдёт за {t} секунд?"
        
        solution = (
            f"📌 **Формула:** S = v × t\n\n"
            f"📊 **Подстановка:**\n"
            f"• v = {v} м/с\n"
            f"• t = {t} с\n\n"
            f"📝 **Решение:**\n"
            f"1. Записываем формулу: S = v × t\n"
            f"2. Подставляем значения: S = {v} × {t}\n"
            f"3. Вычисляем: S = {s} м\n\n"
            f"✅ **Ответ:** Расстояние S = {s} м"
        )
        
        return task, solution
    
    def mech_accelerated_motion(self):
        """Равноускоренное движение"""
        v0 = random.randint(5, 20)
        a = round(random.uniform(1.0, 4.0), 1)
        t = random.randint(3, 12)
        v = v0 + a * t
        s = v0 * t + 0.5 * a * t**2
        
        task = (f"🏃 Автомобиль начал движение со скоростью {v0} м/с "
                f"и разгоняется с ускорением {a} м/с² в течение {t} с. "
                f"Найти конечную скорость и пройденный путь.")
        
        solution = (
            f"📌 **Формулы:**\n"
            f"• v = v₀ + at\n"
            f"• S = v₀t + at²/2\n\n"
            f"📊 **Подстановка:**\n"
            f"• v₀ = {v0} м/с\n"
            f"• a = {a} м/с²\n"
            f"• t = {t} с\n\n"
            f"📝 **Решение:**\n"
            f"1. Находим конечную скорость:\n"
            f"   v = {v0} + {a} × {t} = {v:.1f} м/с\n"
            f"2. Находим пройденный путь:\n"
            f"   S = {v0} × {t} + 0.5 × {a} × {t}² = {s:.1f} м\n\n"
            f"✅ **Ответ:** v = {v:.1f} м/с, S = {s:.1f} м"
        )
        
        return task, solution
    
    def mech_second_law(self):
        """Второй закон Ньютона"""
        m = random.randint(2, 20)
        F = random.randint(10, 100)
        a = F / m
        
        task = f"⚡ На тело массой {m} кг действует сила {F} Н. Какое ускорение приобретает тело?"
        
        solution = (
            f"📌 **Формула:** F = m × a  →  a = F/m\n\n"
            f"📊 **Подстановка:**\n"
            f"• F = {F} Н\n"
            f"• m = {m} кг\n\n"
            f"📝 **Решение:**\n"
            f"1. Выражаем ускорение из второго закона Ньютона: a = F/m\n"
            f"2. Подставляем значения: a = {F} / {m}\n"
            f"3. Вычисляем: a = {a:.2f} м/с²\n\n"
            f"✅ **Ответ:** a = {a:.2f} м/с²"
        )
        
        return task, solution
    
    def mech_inclined_plane(self):
        """Движение по наклонной плоскости"""
        m = random.randint(2, 10)
        alpha = random.randint(15, 45)
        mu = round(random.uniform(0.1, 0.5), 2)
        g = 9.8
        a = g * (math.sin(math.radians(alpha)) - mu * math.cos(math.radians(alpha)))
        
        task = (f"⛰️ Тело массой {m} кг соскальзывает с наклонной плоскости "
                f"с углом наклона {alpha}°. Коэффициент трения μ = {mu}. "
                f"Найти ускорение тела (g = 9.8 м/с²).")
        
        solution = (
            f"📌 **Формула:** a = g(sin α - μ cos α)\n\n"
            f"📊 **Подстановка:**\n"
            f"• α = {alpha}°\n"
            f"• μ = {mu}\n"
            f"• g = 9.8 м/с²\n\n"
            f"📝 **Решение:**\n"
            f"1. Вычисляем sin {alpha}° = {math.sin(math.radians(alpha)):.3f}\n"
            f"2. Вычисляем cos {alpha}° = {math.cos(math.radians(alpha)):.3f}\n"
            f"3. Подставляем в формулу:\n"
            f"   a = 9.8 × ({math.sin(math.radians(alpha)):.3f} - {mu} × {math.cos(math.radians(alpha)):.3f})\n"
            f"4. Вычисляем: a = {a:.2f} м/с²\n\n"
            f"✅ **Ответ:** a = {a:.2f} м/с²"
        )
        
        return task, solution
    
    def mech_projectile_motion(self):
        """Движение тела, брошенного под углом"""
        v0 = random.randint(10, 30)
        alpha = random.choice([30, 45, 60])
        g = 9.8
        h_max = (v0**2 * (math.sin(math.radians(alpha))**2)) / (2 * g)
        L = (v0**2 * math.sin(2 * math.radians(alpha))) / g
        
        task = (f"🎯 Мяч брошен под углом {alpha}° к горизонту "
                f"со скоростью {v0} м/с. Найти максимальную высоту "
                f"подъёма и дальность полёта (g = 9.8 м/с²).")
        
        solution = (
            f"📌 **Формулы:**\n"
            f"• h_max = (v₀² sin²α)/(2g)\n"
            f"• L = (v₀² sin 2α)/g\n\n"
            f"📊 **Подстановка:**\n"
            f"• v₀ = {v0} м/с\n"
            f"• α = {alpha}°\n"
            f"• g = 9.8 м/с²\n\n"
            f"📝 **Решение:**\n"
            f"1. Вычисляем sin {alpha}° = {math.sin(math.radians(alpha)):.3f}\n"
            f"2. Вычисляем sin(2×{alpha}°) = {math.sin(2*math.radians(alpha)):.3f}\n"
            f"3. Находим максимальную высоту:\n"
            f"   h_max = ({v0}² × {math.sin(math.radians(alpha)):.3f}²) / (2 × 9.8) = {h_max:.1f} м\n"
            f"4. Находим дальность полёта:\n"
            f"   L = ({v0}² × {math.sin(2*math.radians(alpha)):.3f}) / 9.8 = {L:.1f} м\n\n"
            f"✅ **Ответ:** h_max = {h_max:.1f} м, L = {L:.1f} м"
        )
        
        return task, solution
    
    def mech_collision(self):
        """Неупругое столкновение"""
        m1 = random.randint(2, 8)
        v1 = random.randint(5, 15)
        m2 = random.randint(3, 10)
        v = (m1 * v1) / (m1 + m2)
        
        task = (f"💥 Тело массой {m1} кг движется со скоростью {v1} м/с "
                f"и сталкивается с неподвижным телом массой {m2} кг. "
                f"Столкновение абсолютно неупругое. Найти скорость тел после удара.")
        
        solution = (
            f"📌 **Формула:** v = (m₁v₁ + m₂v₂)/(m₁ + m₂), v₂ = 0\n\n"
            f"📊 **Подстановка:**\n"
            f"• m₁ = {m1} кг\n"
            f"• v₁ = {v1} м/с\n"
            f"• m₂ = {m2} кг\n"
            f"• v₂ = 0 м/с\n\n"
            f"📝 **Решение:**\n"
            f"1. Используем закон сохранения импульса: m₁v₁ + m₂v₂ = (m₁ + m₂)v\n"
            f"2. Так как второе тело покоится: m₁v₁ = (m₁ + m₂)v\n"
            f"3. Выражаем v = (m₁v₁)/(m₁ + m₂)\n"
            f"4. Подставляем: v = ({m1} × {v1})/({m1} + {m2})\n"
            f"5. Вычисляем: v = {v:.2f} м/с\n\n"
            f"✅ **Ответ:** v = {v:.2f} м/с"
        )
        
        return task, solution
    
    def mech_energy(self):
        """Кинетическая и потенциальная энергия"""
        m = random.randint(2, 15)
        h = random.randint(5, 25)
        v = random.randint(3, 12)
        g = 9.8
        Ep = m * g * h
        Ek = 0.5 * m * v**2
        
        task = (f"🏗️ Груз массой {m} кг поднят на высоту {h} м "
                f"и движется со скоростью {v} м/с. "
                f"Найти потенциальную и кинетическую энергию (g = 9.8 м/с²).")
        
        solution = (
            f"📌 **Формулы:**\n"
            f"• Ep = mgh\n"
            f"• Ek = mv²/2\n\n"
            f"📊 **Подстановка:**\n"
            f"• m = {m} кг\n"
            f"• h = {h} м\n"
            f"• v = {v} м/с\n"
            f"• g = 9.8 м/с²\n\n"
            f"📝 **Решение:**\n"
            f"1. Потенциальная энергия:\n"
            f"   Ep = {m} × 9.8 × {h} = {Ep:.0f} Дж\n"
            f"2. Кинетическая энергия:\n"
            f"   Ek = 0.5 × {m} × {v}² = {Ek:.0f} Дж\n\n"
            f"✅ **Ответ:** Ep = {Ep:.0f} Дж, Ek = {Ek:.0f} Дж"
        )
        
        return task, solution
    
    def mech_circular_motion(self):
        """Движение по окружности"""
        m = random.randint(1, 5)
        v = random.randint(5, 15)
        r = random.randint(2, 10)
        F = m * v**2 / r
        
        task = (f"🔄 Тело массой {m} кг движется по окружности "
                f"радиусом {r} м со скоростью {v} м/с. "
                f"Найти центростремительную силу.")
        
        solution = (
            f"📌 **Формула:** F = mv²/r\n\n"
            f"📊 **Подстановка:**\n"
            f"• m = {m} кг\n"
            f"• v = {v} м/с\n"
            f"• r = {r} м\n\n"
            f"📝 **Решение:**\n"
            f"1. Центростремительная сила: F = mv²/r\n"
            f"2. Подставляем: F = {m} × {v}² / {r}\n"
            f"3. Вычисляем: F = {F:.1f} Н\n\n"
            f"✅ **Ответ:** F = {F:.1f} Н"
        )
        
        return task, solution
    
    def mech_pendulum(self):
        """Математический маятник"""
        L = round(random.uniform(0.5, 2.5), 2)
        g = 9.8
        T = 2 * math.pi * math.sqrt(L / g)
        
        task = f"⏰ Математический маятник имеет длину {L} м. Найти период колебаний (g = 9.8 м/с²)."
        
        solution = (
            f"📌 **Формула:** T = 2π √(L/g)\n\n"
            f"📊 **Подстановка:**\n"
            f"• L = {L} м\n"
            f"• g = 9.8 м/с²\n"
            f"• π ≈ 3.14\n\n"
            f"📝 **Решение:**\n"
            f"1. Вычисляем L/g = {L:.2f}/9.8 = {L/9.8:.3f}\n"
            f"2. Извлекаем корень: √{L/9.8:.3f} = {math.sqrt(L/9.8):.3f}\n"
            f"3. Умножаем на 2π: T = 2 × 3.14 × {math.sqrt(L/9.8):.3f}\n"
            f"4. Получаем: T = {T:.2f} с\n\n"
            f"✅ **Ответ:** T = {T:.2f} с"
        )
        
        return task, solution
    
    def mech_lever(self):
        """Правило рычага"""
        F1 = random.randint(20, 100)
        d1 = random.randint(1, 5)
        F2 = random.randint(30, 150)
        d2 = (F1 * d1) / F2
        
        task = (f"⚖️ К левому плечу рычага длиной {d1} м приложена сила {F1} Н. "
                f"Какую силу нужно приложить к правому плечу длиной {d2:.1f} м для равновесия?")
        
        solution = (
            f"📌 **Формула:** F₁d₁ = F₂d₂  →  F₂ = F₁d₁/d₂\n\n"
            f"📊 **Подстановка:**\n"
            f"• F₁ = {F1} Н\n"
            f"• d₁ = {d1} м\n"
            f"• d₂ = {d2:.1f} м\n\n"
            f"📝 **Решение:**\n"
            f"1. Используем правило моментов: F₁d₁ = F₂d₂\n"
            f"2. Выражаем F₂ = F₁d₁/d₂\n"
            f"3. Подставляем: F₂ = {F1} × {d1} / {d2:.1f}\n"
            f"4. Вычисляем: F₂ = {F2:.0f} Н\n\n"
            f"✅ **Ответ:** F₂ = {F2:.0f} Н"
        )
        
        return task, solution
    
    def mech_pressure(self):
        """Давление жидкости"""
        h1 = round(random.uniform(0.5, 2.0), 1)
        h2 = round(random.uniform(0.3, 1.5), 1)
        rho1 = 1000
        rho2 = 800
        g = 9.8
        p = rho1 * g * h1 + rho2 * g * h2
        
        task = (f"🌊 В сосуд налиты вода (ρ = 1000 кг/м³) высотой {h1} м "
                f"и масло (ρ = 800 кг/м³) высотой {h2} м. "
                f"Найти давление на дно сосуда (g = 9.8 м/с²).")
        
        solution = (
            f"📌 **Формула:** p = ρ₁gh₁ + ρ₂gh₂\n\n"
            f"📊 **Подстановка:**\n"
            f"• ρ₁ = 1000 кг/м³\n"
            f"• h₁ = {h1} м\n"
            f"• ρ₂ = 800 кг/м³\n"
            f"• h₂ = {h2} м\n"
            f"• g = 9.8 м/с²\n\n"
            f"📝 **Решение:**\n"
            f"1. Давление воды: p₁ = 1000 × 9.8 × {h1} = {rho1*g*h1:.0f} Па\n"
            f"2. Давление масла: p₂ = 800 × 9.8 × {h2} = {rho2*g*h2:.0f} Па\n"
            f"3. Общее давление: p = {rho1*g*h1:.0f} + {rho2*g*h2:.0f} = {p:.0f} Па\n\n"
            f"✅ **Ответ:** p = {p:.0f} Па"
        )
        
        return task, solution
    
    def mech_springs(self):
        """Последовательное соединение пружин"""
        k1 = random.randint(100, 300)
        k2 = random.randint(150, 400)
        x = round(random.uniform(0.05, 0.15), 3)
        k_eq = (k1 * k2) / (k1 + k2)
        F = k_eq * x
        
        task = (f"🔩 Две пружины жёсткостью {k1} Н/м и {k2} Н/м "
                f"соединены последовательно и растянуты на {x*100:.1f} см. "
                f"Найти силу упругости.")
        
        solution = (
            f"📌 **Формулы:**\n"
            f"• k_eq = (k₁k₂)/(k₁ + k₂)\n"
            f"• F = k_eq·x\n\n"
            f"📊 **Подстановка:**\n"
            f"• k₁ = {k1} Н/м\n"
            f"• k₂ = {k2} Н/м\n"
            f"• x = {x} м\n\n"
            f"📝 **Решение:**\n"
            f"1. Находим эквивалентную жёсткость:\n"
            f"   k_eq = ({k1} × {k2})/({k1} + {k2}) = {k_eq:.0f} Н/м\n"
            f"2. Находим силу упругости:\n"
            f"   F = {k_eq:.0f} × {x} = {F:.1f} Н\n\n"
            f"✅ **Ответ:** F = {F:.1f} Н"
        )
        
        return task, solution
    
    # ============= ТЕРМОДИНАМИКА =============
    
    def thermo_ideal_gas(self):
        """Идеальный газ"""
        p = random.randint(100, 300) * 1000
        V = round(random.uniform(0.5, 3.0), 2)
        T = random.randint(273, 373)
        R = 8.31
        n = p * V / (R * T)
        
        task = (f"🧪 В сосуде объёмом {V} м³ находится газ "
                f"под давлением {p/1000:.0f} кПа при температуре {T} К. "
                f"Найти количество вещества (в молях).")
        
        solution = (
            f"📌 **Формула:** pV = nRT  →  n = pV/(RT)\n\n"
            f"📊 **Подстановка:**\n"
            f"• p = {p} Па\n"
            f"• V = {V} м³\n"
            f"• T = {T} К\n"
            f"• R = 8.31 Дж/(моль·К)\n\n"
            f"📝 **Решение:**\n"
            f"1. Выражаем n из уравнения Менделеева-Клапейрона: n = pV/(RT)\n"
            f"2. Подставляем: n = ({p} × {V})/(8.31 × {T})\n"
            f"3. Вычисляем: n = {n:.2f} моль\n\n"
            f"✅ **Ответ:** n = {n:.2f} моль"
        )
        
        return task, solution
    
    def thermo_isobaric(self):
        """Изобарный процесс"""
        V1 = random.randint(2, 10)
        V2 = random.randint(12, 30)
        T1 = random.randint(280, 340)
        T2 = int(T1 * V2 / V1)
        p = random.randint(100, 200) * 1000
        A = p * (V2 - V1) * 0.001
        
        task = (f"🔥 Газ изобарно расширяется от {V1} л до {V2} л. "
                f"Начальная температура {T1} К, давление {p/1000:.0f} кПа. "
                f"Найти конечную температуру и работу газа.")
        
        solution = (
            f"📌 **Формулы:**\n"
            f"• V₁/T₁ = V₂/T₂\n"
            f"• A = pΔV\n\n"
            f"📊 **Подстановка:**\n"
            f"• V₁ = {V1} л\n"
            f"• V₂ = {V2} л\n"
            f"• T₁ = {T1} К\n"
            f"• p = {p/1000:.0f} кПа\n\n"
            f"📝 **Решение:**\n"
            f"1. Находим конечную температуру:\n"
            f"   T₂ = T₁ × V₂/V₁ = {T1} × {V2}/{V1} = {T2} К\n"
            f"2. Находим работу газа:\n"
            f"   A = pΔV = {p/1000:.0f} × ({V2}-{V1}) × 0.001 = {A:.0f} Дж\n\n"
            f"✅ **Ответ:** T₂ = {T2} К, A = {A:.0f} Дж"
        )
        
        return task, solution
    
    def thermo_heat_capacity(self):
        """Теплоёмкость"""
        m = random.randint(1, 5)
        materials = {4200: "воды", 900: "алюминия", 460: "железа"}
        c = random.choice([4200, 900, 460])
        dT = random.randint(10, 50)
        Q = m * c * dT
        material = materials[c]
        
        task = (f"🌡️ Для нагревания {m} кг {material} на {dT}°C "
                f"потребовалось некоторое количество теплоты. "
                f"Найти это количество (c = {c} Дж/(кг·°C)).")
        
        solution = (
            f"📌 **Формула:** Q = mcΔT\n\n"
            f"📊 **Подстановка:**\n"
            f"• m = {m} кг\n"
            f"• c = {c} Дж/(кг·°C)\n"
            f"• ΔT = {dT} °C\n\n"
            f"📝 **Решение:**\n"
            f"1. Подставляем в формулу: Q = {m} × {c} × {dT}\n"
            f"2. Вычисляем: Q = {Q} Дж = {Q/1000:.1f} кДж\n\n"
            f"✅ **Ответ:** Q = {Q} Дж ({Q/1000:.1f} кДж)"
        )
        
        return task, solution
    
    def thermo_first_law(self):
        """Первый закон термодинамики"""
        Q = random.randint(1000, 5000)
        A = random.randint(300, 2000)
        dU = Q - A
        
        task = (f"📊 Газу передано {Q} Дж теплоты. "
                f"При этом газ совершил работу {A} Дж. "
                f"Найти изменение внутренней энергии газа.")
        
        solution = (
            f"📌 **Формула:** ΔU = Q - A\n\n"
            f"📊 **Подстановка:**\n"
            f"• Q = {Q} Дж\n"
            f"• A = {A} Дж\n\n"
            f"📝 **Решение:**\n"
            f"1. Первый закон термодинамики: ΔU = Q - A\n"
            f"2. Подставляем: ΔU = {Q} - {A}\n"
            f"3. Вычисляем: ΔU = {dU} Дж\n\n"
            f"✅ **Ответ:** ΔU = {dU} Дж"
        )
        
        return task, solution
    
    def thermo_carnot(self):
        """Цикл Карно"""
        T1 = random.randint(500, 800)
        T2 = random.randint(300, 450)
        eta = (1 - T2/T1) * 100
        
        task = (f"🔄 Тепловая машина работает по циклу Карно "
                f"с температурой нагревателя {T1} К и холодильника {T2} К. "
                f"Найти КПД машины.")
        
        solution = (
            f"📌 **Формула:** η = (1 - T₂/T₁) × 100%\n\n"
            f"📊 **Подстановка:**\n"
            f"• T₁ = {T1} К\n"
            f"• T₂ = {T2} К\n\n"
            f"📝 **Решение:**\n"
            f"1. Вычисляем отношение T₂/T₁ = {T2}/{T1} = {T2/T1:.3f}\n"
            f"2. Подставляем: η = (1 - {T2/T1:.3f}) × 100%\n"
            f"3. Вычисляем: η = {eta:.1f}%\n\n"
            f"✅ **Ответ:** η = {eta:.1f}%"
        )
        
        return task, solution
    
    def thermo_phase_change(self):
        """Фазовый переход"""
        m = random.randint(1, 3)
        L = 334000
        Q = m * L
        
        task = (f"❄️ Для плавления {m} кг льда, взятого при 0°C, "
                f"требуется некоторое количество теплоты. "
                f"Найти это количество (λ = 334 кДж/кг).")
        
        solution = (
            f"📌 **Формула:** Q = m·λ\n\n"
            f"📊 **Подстановка:**\n"
            f"• m = {m} кг\n"
            f"• λ = 334000 Дж/кг\n\n"
            f"📝 **Решение:**\n"
            f"1. Подставляем в формулу: Q = {m} × 334000\n"
            f"2. Вычисляем: Q = {Q} Дж = {Q/1000:.0f} кДж\n\n"
            f"✅ **Ответ:** Q = {Q/1000:.0f} кДж"
        )
        
        return task, solution
    
    def thermo_work(self):
        """Работа газа"""
        p = random.randint(150, 300) * 1000
        dV = round(random.uniform(0.2, 1.5), 2)
        A = p * dV
        
        task = (f"⚙️ Газ изобарно расширяется при давлении {p/1000:.0f} кПа, "
                f"увеличивая объём на {dV} м³. "
                f"Найти работу, совершённую газом.")
        
        solution = (
            f"📌 **Формула:** A = p·ΔV\n\n"
            f"📊 **Подстановка:**\n"
            f"• p = {p} Па\n"
            f"• ΔV = {dV} м³\n\n"
            f"📝 **Решение:**\n"
            f"1. Работа газа при изобарном процессе: A = p·ΔV\n"
            f"2. Подставляем: A = {p} × {dV}\n"
            f"3. Вычисляем: A = {A:.0f} Дж\n\n"
            f"✅ **Ответ:** A = {A:.0f} Дж"
        )
        
        return task, solution
    
    def thermo_adiabatic(self):
        """Адиабатный процесс"""
        V1 = random.randint(3, 8)
        V2 = round(V1 * random.uniform(2, 4), 1)
        p1 = random.randint(100, 200) * 1000
        gamma = 1.4
        p2 = p1 * (V1 / V2)**gamma
        
        task = (f"📈 Газ адиабатно сжимают от объёма {V1} л до {V2:.1f} л. "
                f"Начальное давление {p1/1000:.0f} кПа, γ = 1.4. "
                f"Найти конечное давление.")
        
        solution = (
            f"📌 **Формула:** p₁V₁^γ = p₂V₂^γ  →  p₂ = p₁(V₁/V₂)^γ\n\n"
            f"📊 **Подстановка:**\n"
            f"• p₁ = {p1/1000:.0f} кПа\n"
            f"• V₁ = {V1} л\n"
            f"• V₂ = {V2:.1f} л\n"
            f"• γ = 1.4\n\n"
            f"📝 **Решение:**\n"
            f"1. Находим отношение объёмов: V₁/V₂ = {V1}/{V2:.1f} = {V1/V2:.3f}\n"
            f"2. Возводим в степень γ: ({V1/V2:.3f})^{1.4} = {(V1/V2)**gamma:.3f}\n"
            f"3. Умножаем на начальное давление:\n"
            f"   p₂ = {p1/1000:.0f} × {(V1/V2)**gamma:.3f} = {p2/1000:.0f} кПа\n\n"
            f"✅ **Ответ:** p₂ = {p2/1000:.0f} кПа"
        )
        
        return task, solution
    
    def thermo_isochoric(self):
        """Изохорный процесс"""
        n = random.randint(1, 4)
        Cv = 20.8
        dT = random.randint(20, 60)
        Q = n * Cv * dT
        
        task = (f"🧊 {n} моль двухатомного газа нагревают изохорно на {dT} К. "
                f"Найти количество подведённой теплоты (Cv = 20.8 Дж/(моль·К)).")
        
        solution = (
            f"📌 **Формула:** Q = n·Cv·ΔT\n\n"
            f"📊 **Подстановка:**\n"
            f"• n = {n} моль\n"
            f"• Cv = 20.8 Дж/(моль·К)\n"
            f"• ΔT = {dT} К\n\n"
            f"📝 **Решение:**\n"
            f"1. При изохорном процессе вся теплота идёт на изменение внутренней энергии\n"
            f"2. Подставляем: Q = {n} × 20.8 × {dT}\n"
            f"3. Вычисляем: Q = {Q:.0f} Дж\n\n"
            f"✅ **Ответ:** Q = {Q:.0f} Дж"
        )
        
        return task, solution
    
    def thermo_humidity(self):
        """Влажность воздуха"""
        phi = random.randint(40, 90)
        p_sat = random.randint(15, 40) * 100
        p = phi / 100 * p_sat
        
        task = (f"💧 Относительная влажность воздуха {phi}%. "
                f"Давление насыщенного пара при данной температуре {p_sat/100:.1f} кПа. "
                f"Найти парциальное давление водяного пара.")
        
        solution = (
            f"📌 **Формула:** φ = p/p_нас × 100%  →  p = φ·p_нас/100\n\n"
            f"📊 **Подстановка:**\n"
            f"• φ = {phi}%\n"
            f"• p_нас = {p_sat/100:.1f} кПа\n\n"
            f"📝 **Решение:**\n"
            f"1. Выражаем парциальное давление: p = φ·p_нас/100\n"
            f"2. Подставляем: p = {phi} × {p_sat/100:.1f} / 100\n"
            f"3. Вычисляем: p = {p/100:.1f} кПа\n\n"
            f"✅ **Ответ:** p = {p/100:.1f} кПа"
        )
        
        return task, solution
    
    def thermo_mixture(self):
        """Смесь газов"""
        n1 = random.randint(1, 3)
        n2 = random.randint(1, 3)
        dT = random.randint(20, 50)
        Cv1 = 12.5
        Cv2 = 20.8
        dU = n1 * Cv1 * dT + n2 * Cv2 * dT
        
        task = (f"🧪 Смесь из {n1} моль одноатомного и {n2} моль двухатомного газа "
                f"нагревают на {dT} К. Найти изменение внутренней энергии.")
        
        solution = (
            f"📌 **Формула:** ΔU = n₁Cv₁ΔT + n₂Cv₂ΔT\n\n"
            f"📊 **Подстановка:**\n"
            f"• n₁ = {n1} моль\n"
            f"• Cv₁ = 12.5 Дж/(моль·К)\n"
            f"• n₂ = {n2} моль\n"
            f"• Cv₂ = 20.8 Дж/(моль·К)\n"
            f"• ΔT = {dT} К\n\n"
            f"📝 **Решение:**\n"
            f"1. Изменение энергии для одноатомного газа:\n"
            f"   ΔU₁ = {n1} × 12.5 × {dT} = {n1*Cv1*dT:.0f} Дж\n"
            f"2. Изменение энергии для двухатомного газа:\n"
            f"   ΔU₂ = {n2} × 20.8 × {dT} = {n2*Cv2*dT:.0f} Дж\n"
            f"3. Суммарное изменение:\n"
            f"   ΔU = {n1*Cv1*dT:.0f} + {n2*Cv2*dT:.0f} = {dU:.0f} Дж\n\n"
            f"✅ **Ответ:** ΔU = {dU:.0f} Дж"
        )
        
        return task, solution
    
    def thermo_dalton(self):
        """Закон Дальтона"""
        p1 = random.randint(30, 70) * 1000
        p2 = random.randint(40, 80) * 1000
        p = p1 + p2
        
        task = (f"🧪 В сосуде находится смесь двух газов. "
                f"Парциальные давления газов: {p1/1000:.0f} кПа и {p2/1000:.0f} кПа. "
                f"Найти общее давление смеси.")
        
        solution = (
            f"📌 **Формула:** p = p₁ + p₂ (закон Дальтона)\n\n"
            f"📊 **Подстановка:**\n"
            f"• p₁ = {p1/1000:.0f} кПа\n"
            f"• p₂ = {p2/1000:.0f} кПа\n\n"
            f"📝 **Решение:**\n"
            f"1. Закон Дальтона: давление смеси равно сумме парциальных давлений\n"
            f"2. Складываем: p = {p1/1000:.0f} + {p2/1000:.0f} = {p/1000:.0f} кПа\n\n"
            f"✅ **Ответ:** p = {p/1000:.0f} кПа"
        )
        
        return task, solution
    
    # ============= ЭЛЕКТРОДИНАМИКА =============
    
    def electro_coulomb(self):
        """Закон Кулона"""
        q1 = random.randint(2, 10) * 10**-6
        q2 = random.randint(3, 12) * 10**-6
        r = random.randint(5, 30) * 0.01
        k = 9 * 10**9
        F = k * abs(q1 * q2) / r**2
        
        task = (f"⚡ Два точечных заряда {q1*10**6:.0f} мкКл и {q2*10**6:.0f} мкКл "
                f"находятся на расстоянии {r*100:.0f} см друг от друга. "
                f"Найти силу взаимодействия (k = 9·10⁹ Н·м²/Кл²).")
        
        solution = (
            f"📌 **Формула:** F = k·|q₁·q₂|/r²\n\n"
            f"📊 **Подстановка:**\n"
            f"• q₁ = {q1*10**6:.0f} мкКл = {q1:.2e} Кл\n"
            f"• q₂ = {q2*10**6:.0f} мкКл = {q2:.2e} Кл\n"
            f"• r = {r*100:.0f} см = {r:.2f} м\n"
            f"• k = 9·10⁹ Н·м²/Кл²\n\n"
            f"📝 **Решение:**\n"
            f"1. Подставляем в закон Кулона:\n"
            f"   F = 9·10⁹ × ({q1:.2e} × {q2:.2e}) / {r:.2f}²\n"
            f"2. Вычисляем: F = {F:.2f} Н\n\n"
            f"✅ **Ответ:** F = {F:.2f} Н"
        )
        
        return task, solution
    
    def electro_field(self):
        """Напряжённость поля"""
        q = random.randint(5, 20) * 10**-6
        r = random.randint(10, 50) * 0.01
        k = 9 * 10**9
        E = k * abs(q) / r**2
        
        task = (f"⚡ Найти напряжённость электрического поля, "
                f"создаваемого зарядом {q*10**6:.0f} мкКл на расстоянии {r*100:.0f} см.")
        
        solution = (
            f"📌 **Формула:** E = k·|q|/r²\n\n"
            f"📊 **Подстановка:**\n"
            f"• q = {q*10**6:.0f} мкКл = {q:.2e} Кл\n"
            f"• r = {r*100:.0f} см = {r:.2f} м\n"
            f"• k = 9·10⁹ Н·м²/Кл²\n\n"
            f"📝 **Решение:**\n"
            f"1. Подставляем в формулу напряжённости:\n"
            f"   E = 9·10⁹ × {q:.2e} / {r:.2f}²\n"
            f"2. Вычисляем: E = {E:.0f} В/м\n\n"
            f"✅ **Ответ:** E = {E:.0f} В/м"
        )
        
        return task, solution
    
    def electro_ohm(self):
        """Закон Ома"""
        U = random.randint(12, 220)
        R = random.randint(10, 100)
        I = U / R
        
        task = (f"💡 К участку цепи приложено напряжение {U} В. "
                f"Сопротивление участка {R} Ом. Найти силу тока.")
        
        solution = (
            f"📌 **Формула:** I = U/R\n\n"
            f"📊 **Подстановка:**\n"
            f"• U = {U} В\n"
            f"• R = {R} Ом\n\n"
            f"📝 **Решение:**\n"
            f"1. Закон Ома: I = U/R\n"
            f"2. Подставляем: I = {U} / {R}\n"
            f"3. Вычисляем: I = {I:.2f} А\n\n"
            f"✅ **Ответ:** I = {I:.2f} А"
        )
        
        return task, solution
    
    def electro_power(self):
        """Мощность тока"""
        I = round(random.uniform(1.0, 5.0), 1)
        U = random.randint(110, 220)
        P = I * U
        
        task = (f"💡 Электрический прибор потребляет ток {I} А "
                f"при напряжении {U} В. Найти мощность прибора.")
        
        solution = (
            f"📌 **Формула:** P = U·I\n\n"
            f"📊 **Подстановка:**\n"
            f"• U = {U} В\n"
            f"• I = {I} А\n\n"
            f"📝 **Решение:**\n"
            f"1. Мощность электрического тока: P = U·I\n"
            f"2. Подставляем: P = {U} × {I}\n"
            f"3. Вычисляем: P = {P:.0f} Вт\n\n"
            f"✅ **Ответ:** P = {P:.0f} Вт"
        )
        
        return task, solution
    
    def electro_series(self):
        """Последовательное соединение"""
        R1 = random.randint(10, 50)
        R2 = random.randint(20, 80)
        R = R1 + R2
        
        task = (f"🔌 Два резистора соединены последовательно: "
                f"R₁ = {R1} Ом, R₂ = {R2} Ом. Найти общее сопротивление.")
        
        solution = (
            f"📌 **Формула:** R = R₁ + R₂\n\n"
            f"📊 **Подстановка:**\n"
            f"• R₁ = {R1} Ом\n"
            f"• R₂ = {R2} Ом\n\n"
            f"📝 **Решение:**\n"
            f"1. При последовательном соединении сопротивления складываются\n"
            f"2. R = {R1} + {R2} = {R} Ом\n\n"
            f"✅ **Ответ:** R = {R} Ом"
        )
        
        return task, solution
    
    def electro_parallel(self):
        """Параллельное соединение"""
        R1 = random.randint(10, 40)
        R2 = random.randint(15, 60)
        R = 1 / (1/R1 + 1/R2)
        
        task = (f"🔌 Два резистора соединены параллельно: "
                f"R₁ = {R1} Ом, R₂ = {R2} Ом. Найти общее сопротивление.")
        
        solution = (
            f"📌 **Формула:** 1/R = 1/R₁ + 1/R₂\n\n"
            f"📊 **Подстановка:**\n"
            f"• R₁ = {R1} Ом\n"
            f"• R₂ = {R2} Ом\n\n"
            f"📝 **Решение:**\n"
            f"1. При параллельном соединении: 1/R = 1/R₁ + 1/R₂\n"
            f"2. Вычисляем: 1/R = 1/{R1} + 1/{R2} = {1/R1:.3f} + {1/R2:.3f} = {1/R1+1/R2:.3f}\n"
            f"3. Находим R = 1 / {1/R1+1/R2:.3f} = {R:.1f} Ом\n\n"
            f"✅ **Ответ:** R = {R:.1f} Ом"
        )
        
        return task, solution
    
    def electro_work(self):
        """Работа тока"""
        P = random.randint(100, 1000)
        t = random.randint(600, 3600)
        A = P * t
        A_kwh = A / 3600000
        
        task = (f"⚡ Электроприбор мощностью {P} Вт работал {t//60} минут. "
                f"Найти работу тока в кВт·ч.")
        
        solution = (
            f"📌 **Формула:** A = P·t\n\n"
            f"📊 **Подстановка:**\n"
            f"• P = {P} Вт\n"
            f"• t = {t} с\n\n"
            f"📝 **Решение:**\n"
            f"1. Работа электрического тока: A = P·t\n"
            f"2. A = {P} × {t} = {A} Дж\n"
            f"3. Переводим в кВт·ч: {A} / 3600000 = {A_kwh:.2f} кВт·ч\n\n"
            f"✅ **Ответ:** A = {A_kwh:.2f} кВт·ч"
        )
        
        return task, solution
    
    def electro_capacitor(self):
        """Конденсатор"""
        C = random.randint(10, 100) * 10**-6
        U = random.randint(50, 300)
        q = C * U
        
        task = (f"🔋 Конденсатор ёмкостью {C*10**6:.0f} мкФ заряжен "
                f"до напряжения {U} В. Найти заряд конденсатора.")
        
        solution = (
            f"📌 **Формула:** q = C·U\n\n"
            f"📊 **Подстановка:**\n"
            f"• C = {C*10**6:.0f} мкФ = {C:.2e} Ф\n"
            f"• U = {U} В\n\n"
            f"📝 **Решение:**\n"
            f"1. Заряд конденсатора: q = C·U\n"
            f"2. Подставляем: q = {C:.2e} × {U}\n"
            f"3. Вычисляем: q = {q*10**6:.1f} мкКл\n\n"
            f"✅ **Ответ:** q = {q*10**6:.1f} мкКл"
        )
        
        return task, solution
    
    def electro_ampere(self):
        """Сила Ампера"""
        I = random.randint(2, 10)
        L = random.randint(10, 50) * 0.01
        B = round(random.uniform(0.05, 0.30), 2)
        F = B * I * L
        
        task = (f"🧲 На проводник с током {I} А длиной {L*100:.0f} см "
                f"в магнитном поле с индукцией {B} Тл действует сила Ампера. "
                f"Найти эту силу (поле перпендикулярно проводнику).")
        
        solution = (
            f"📌 **Формула:** F = B·I·L·sin α, α = 90°\n\n"
            f"📊 **Подстановка:**\n"
            f"• B = {B} Тл\n"
            f"• I = {I} А\n"
            f"• L = {L} м\n"
            f"• sin 90° = 1\n\n"
            f"📝 **Решение:**\n"
            f"1. Сила Ампера: F = B·I·L·sin α\n"
            f"2. Так как поле перпендикулярно, sin 90° = 1\n"
            f"3. Подставляем: F = {B} × {I} × {L}\n"
            f"4. Вычисляем: F = {F:.2f} Н\n\n"
            f"✅ **Ответ:** F = {F:.2f} Н"
        )
        
        return task, solution
    
    def electro_induction(self):
        """ЭДС индукции"""
        dPhi = round(random.uniform(0.1, 0.8), 2)
        dt = round(random.uniform(0.05, 0.25), 3)
        eps = dPhi / dt
        
        task = (f"🔄 Магнитный поток через контур изменился на {dPhi} Вб "
                f"за время {dt*1000:.0f} мс. Найти ЭДС индукции.")
        
        solution = (
            f"📌 **Формула:** |ℰ| = ΔΦ/Δt\n\n"
            f"📊 **Подстановка:**\n"
            f"• ΔΦ = {dPhi} Вб\n"
            f"• Δt = {dt} с\n\n"
            f"📝 **Решение:**\n"
            f"1. Закон электромагнитной индукции: |ℰ| = ΔΦ/Δt\n"
            f"2. Подставляем: |ℰ| = {dPhi} / {dt}\n"
            f"3. Вычисляем: |ℰ| = {eps:.1f} В\n\n"
            f"✅ **Ответ:** ℰ = {eps:.1f} В"
        )
        
        return task, solution
    
    def electro_magnetic_field(self):
        """Магнитное поле прямого тока"""
        I = random.randint(5, 20)
        r = random.randint(5, 25) * 0.01
        B = 2e-7 * I / r
        
        task = (f"🧲 Найти индукцию магнитного поля на расстоянии {r*100:.0f} см "
                f"от прямого провода с током {I} А.")
        
        solution = (
            f"📌 **Формула:** B = μ₀I/(2πr) = 2·10⁻⁷·I/r\n\n"
            f"📊 **Подстановка:**\n"
            f"• I = {I} А\n"
            f"• r = {r} м\n\n"
            f"📝 **Решение:**\n"
            f"1. Индукция поля прямого тока: B = 2·10⁻⁷·I/r\n"
            f"2. Подставляем: B = 2·10⁻⁷ × {I} / {r}\n"
            f"3. Вычисляем: B = {B*10**4:.1f}·10⁻⁴ Тл = {B*10**4:.1f} мТл\n\n"
            f"✅ **Ответ:** B = {B*10**4:.1f} мТл"
        )
        
        return task, solution
    
    def electro_joule(self):
        """Закон Джоуля-Ленца"""
        I = round(random.uniform(1.0, 6.0), 1)
        R = random.randint(10, 50)
        t = random.randint(60, 600)
        Q = I**2 * R * t
        
        task = (f"🔥 По проводнику сопротивлением {R} Ом "
                f"течёт ток {I} А в течение {t} с. "
                f"Найти количество выделившейся теплоты.")
        
        solution = (
            f"📌 **Формула:** Q = I²·R·t\n\n"
            f"📊 **Подстановка:**\n"
            f"• I = {I} А\n"
            f"• R = {R} Ом\n"
            f"• t = {t} с\n\n"
            f"📝 **Решение:**\n"
            f"1. Закон Джоуля-Ленца: Q = I²·R·t\n"
            f"2. I² = {I}² = {I**2:.2f}\n"
            f"3. Подставляем: Q = {I**2:.2f} × {R} × {t}\n"
            f"4. Вычисляем: Q = {Q:.0f} Дж = {Q/1000:.1f} кДж\n\n"
            f"✅ **Ответ:** Q = {Q:.0f} Дж ({Q/1000:.1f} кДж)"
        )
        
        return task, solution
    
    # ============= ОПТИКА =============
    
    def optics_reflection(self):
        """Отражение света"""
        i = random.randint(20, 70)
        
        task = (f"🪞 Луч света падает на плоское зеркало под углом {i}°. "
                f"Найти угол отражения.")
        
        solution = (
            f"📌 **Формула:** α = β (закон отражения)\n\n"
            f"📊 **Подстановка:**\n"
            f"• α = {i}°\n\n"
            f"📝 **Решение:**\n"
            f"1. Закон отражения: угол падения равен углу отражения\n"
            f"2. Следовательно, β = α = {i}°\n\n"
            f"✅ **Ответ:** β = {i}°"
        )
        
        return task, solution
    
    def optics_refraction(self):
        """Преломление света"""
        n = round(random.uniform(1.33, 1.60), 2)
        i = random.randint(30, 60)
        r_rad = math.asin(math.sin(math.radians(i)) / n)
        r = math.degrees(r_rad)
        
        task = (f"💧 Луч света переходит из воздуха в среду "
                f"с показателем преломления {n}. Угол падения {i}°. "
                f"Найти угол преломления.")
        
        solution = (
            f"📌 **Формула:** n = sin α / sin β  →  sin β = sin α / n\n\n"
            f"📊 **Подстановка:**\n"
            f"• n = {n}\n"
            f"• α = {i}°\n\n"
            f"📝 **Решение:**\n"
            f"1. sin {i}° = {math.sin(math.radians(i)):.3f}\n"
            f"2. sin β = {math.sin(math.radians(i)):.3f} / {n} = {math.sin(math.radians(i))/n:.3f}\n"
            f"3. β = arcsin({math.sin(math.radians(i))/n:.3f}) = {r:.1f}°\n\n"
            f"✅ **Ответ:** β = {r:.1f}°"
        )
        
        return task, solution
    
    def optics_lens(self):
        """Формула тонкой линзы"""
        f = random.randint(10, 30)
        d = random.randint(20, 80)
        f_ = 1 / (1/f - 1/d)
        
        task = (f"🔍 Собирающая линза с фокусным расстоянием {f} см. "
                f"Предмет находится на расстоянии {d} см от линзы. "
                f"Найти расстояние от линзы до изображения.")
        
        solution = (
            f"📌 **Формула:** 1/F = 1/d + 1/f\n\n"
            f"📊 **Подстановка:**\n"
            f"• F = {f} см\n"
            f"• d = {d} см\n\n"
            f"📝 **Решение:**\n"
            f"1. Выражаем 1/f = 1/F - 1/d\n"
            f"2. 1/f = 1/{f} - 1/{d} = {1/f:.3f} - {1/d:.3f} = {1/f-1/d:.3f}\n"
            f"3. f = 1 / {1/f-1/d:.3f} = {f_:.1f} см\n\n"
            f"✅ **Ответ:** f = {f_:.1f} см"
        )
        
        return task, solution
    
    def optics_magnification(self):
        """Увеличение линзы"""
        f = random.randint(8, 25)
        d = random.randint(15, 50)
        
        if d > f:
            Gamma = f / (d - f)
            result_text = f"Γ = {Gamma:.1f}"
        else:
            Gamma = "мнимое"
            result_text = "Изображение мнимое, прямое"
        
        task = (f"🔍 Лупа с фокусным расстоянием {f} см. "
                f"Предмет находится на расстоянии {d} см от линзы. "
                f"Найти увеличение.")
        
        if d > f:
            solution = (
                f"📌 **Формула:** Γ = f/(d - f)\n\n"
                f"📊 **Подстановка:**\n"
                f"• f = {f} см\n"
                f"• d = {d} см\n\n"
                f"📝 **Решение:**\n"
                f"1. Увеличение линзы: Γ = f/(d - f)\n"
                f"2. Γ = {f} / ({d} - {f}) = {f} / {d-f} = {Gamma:.1f}\n\n"
                f"✅ **Ответ:** Γ = {Gamma:.1f}"
            )
        else:
            solution = (
                f"📌 **Формула:** Γ = f/(d - f)\n\n"
                f"📊 **Подстановка:**\n"
                f"• f = {f} см\n"
                f"• d = {d} см\n\n"
                f"📝 **Решение:**\n"
                f"1. Так как d < f, то d - f < 0, значит изображение мнимое\n"
                f"2. В этом случае линза работает как лупа, давая мнимое изображение\n\n"
                f"✅ **Ответ:** Изображение мнимое, прямое"
            )
        
        return task, solution
    
    def optics_mirror(self):
        """Сферическое зеркало"""
        f = random.randint(10, 30)
        d = random.randint(15, 60)
        f_ = 1 / (1/f - 1/d)
        
        task = (f"🪞 Вогнутое зеркало с фокусным расстоянием {f} см. "
                f"Предмет на расстоянии {d} см от зеркала. "
                f"Найти расстояние до изображения.")
        
        solution = (
            f"📌 **Формула:** 1/F = 1/d + 1/f (для вогнутого зеркала)\n\n"
            f"📊 **Подстановка:**\n"
            f"• F = {f} см\n"
            f"• d = {d} см\n\n"
            f"📝 **Решение:**\n"
            f"1. Выражаем 1/f = 1/F - 1/d\n"
            f"2. 1/f = 1/{f} - 1/{d} = {1/f:.3f} - {1/d:.3f} = {1/f-1/d:.3f}\n"
            f"3. f = 1 / {1/f-1/d:.3f} = {f_:.1f} см\n\n"
            f"✅ **Ответ:** f = {f_:.1f} см"
        )
        
        return task, solution
    
    def optics_interference(self):
        """Интерференция"""
        delta = random.randint(400, 1200) * 10**-9
        lam = 550 * 10**-9
        m = round(delta / lam)
        
        task = (f"🌈 В интерференционном опыте разность хода лучей "
                f"составляет {delta*10**9:.0f} нм. Длина волны света λ = 550 нм. "
                f"Найти порядок интерференционного максимума.")
        
        solution = (
            f"📌 **Формула:** Δ = m·λ  →  m = Δ/λ\n\n"
            f"📊 **Подстановка:**\n"
            f"• Δ = {delta*10**9:.0f} нм\n"
            f"• λ = 550 нм\n\n"
            f"📝 **Решение:**\n"
            f"1. Условие интерференционного максимума: Δ = m·λ\n"
            f"2. m = Δ/λ = {delta*10**9:.0f} / 550 = {m:.0f}\n\n"
            f"✅ **Ответ:** m = {m:.0f}"
        )
        
        return task, solution
    
    def optics_power(self):
        """Оптическая сила"""
        f = round(random.uniform(0.1, 0.5), 2)
        D = 1 / f
        
        task = (f"👓 Линза имеет фокусное расстояние {f*100:.0f} см. "
                f"Найти оптическую силу линзы.")
        
        solution = (
            f"📌 **Формула:** D = 1/F\n\n"
            f"📊 **Подстановка:**\n"
            f"• F = {f} м\n\n"
            f"📝 **Решение:**\n"
            f"1. Оптическая сила линзы: D = 1/F\n"
            f"2. D = 1 / {f} = {D:.1f} дптр\n\n"
            f"✅ **Ответ:** D = {D:.1f} дптр"
        )
        
        return task, solution
    
    def optics_total_reflection(self):
        """Полное внутреннее отражение"""
        n = round(random.uniform(1.4, 1.7), 2)
        alpha_kr = math.degrees(math.asin(1/n))
        
        task = (f"💎 Показатель преломления стекла {n}. "
                f"Найти предельный угол полного внутреннего отражения.")
        
        solution = (
            f"📌 **Формула:** sin α_кр = 1/n\n\n"
            f"📊 **Подстановка:**\n"
            f"• n = {n}\n\n"
            f"📝 **Решение:**\n"
            f"1. sin α_кр = 1/{n} = {1/n:.3f}\n"
            f"2. α_кр = arcsin({1/n:.3f}) = {alpha_kr:.1f}°\n\n"
            f"✅ **Ответ:** α_кр = {alpha_kr:.1f}°"
        )
        
        return task, solution
    
    def optics_wave(self):
        """Скорость волны"""
        f = random.randint(400, 800) * 10**12
        lam = round(random.uniform(400, 700), 0) * 10**-9
        v = f * lam
        
        task = (f"🌊 Свет с частотой {f/10**12:.0f} ТГц имеет длину волны {lam*10**9:.0f} нм. "
                f"Найти скорость света в среде.")
        
        solution = (
            f"📌 **Формула:** v = λ·ν\n\n"
            f"📊 **Подстановка:**\n"
            f"• ν = {f/10**12:.0f}·10¹² Гц\n"
            f"• λ = {lam*10**9:.0f}·10⁻⁹ м\n\n"
            f"📝 **Решение:**\n"
            f"1. Скорость волны: v = λ·ν\n"
            f"2. v = {lam*10**9:.0f}·10⁻⁹ × {f/10**12:.0f}·10¹²\n"
            f"3. v = {v:.2e} м/с\n\n"
            f"✅ **Ответ:** v = {v:.2e} м/с"
        )
        
        return task, solution
    
    def optics_polarization(self):
        """Поляризация"""
        I0 = random.randint(50, 200)
        theta = random.randint(30, 70)
        I = I0 * math.cos(math.radians(theta))**2
        
        task = (f"🎭 Естественный свет интенсивностью {I0} проходит "
                f"через два поляризатора, угол между осями которых {theta}°. "
                f"Найти интенсивность прошедшего света.")
        
        solution = (
            f"📌 **Формула:** I = I₀·cos²θ\n\n"
            f"📊 **Подстановка:**\n"
            f"• I₀ = {I0}\n"
            f"• θ = {theta}°\n\n"
            f"📝 **Решение:**\n"
            f"1. cos {theta}° = {math.cos(math.radians(theta)):.3f}\n"
            f"2. cos²θ = ({math.cos(math.radians(theta)):.3f})² = {math.cos(math.radians(theta))**2:.3f}\n"
            f"3. I = {I0} × {math.cos(math.radians(theta))**2:.3f} = {I:.0f}\n\n"
            f"✅ **Ответ:** I = {I:.0f}"
        )
        
        return task, solution
    
    def optics_dispersion(self):
        """Дисперсия"""
        task = "🌈 Почему белый свет разлагается в спектр при прохождении через призму?"
        
        solution = (
            f"📌 **Явление:** Дисперсия света\n\n"
            f"📝 **Объяснение:**\n"
            f"1. Дисперсия - это зависимость показателя преломления вещества от длины волны света\n"
            f"2. Разные цвета имеют разную длину волны\n"
            f"3. Фиолетовый свет (короткая волна) преломляется сильнее красного (длинная волна)\n"
            f"4. Поэтому белый свет, состоящий из всех цветов, разлагается в спектр\n\n"
            f"✅ **Ответ:** Из-за дисперсии - зависимости показателя преломления от длины волны"
        )
        
        return task, solution
    
    def optics_fiber(self):
        """Оптоволокно"""
        n1 = 1.5
        n2 = round(random.uniform(1.4, 1.48), 2)
        NA = math.sqrt(n1**2 - n2**2)
        alpha_max = math.degrees(math.asin(NA))
        
        task = (f"📡 Оптоволокно имеет показатели преломления "
                f"сердцевины n₁ = {n1} и оболочки n₂ = {n2}. "
                f"Найти максимальный угол ввода луча.")
        
        solution = (
            f"📌 **Формула:** NA = √(n₁² - n₂²), sin α_max = NA\n\n"
            f"📊 **Подстановка:**\n"
            f"• n₁ = {n1}\n"
            f"• n₂ = {n2}\n\n"
            f"📝 **Решение:**\n"
            f"1. Числовая апертура: NA = √({n1}² - {n2}²)\n"
            f"2. NA = √({n1**2:.2f} - {n2**2:.2f}) = √{n1**2 - n2**2:.3f} = {NA:.3f}\n"
            f"3. Максимальный угол: sin α_max = NA = {NA:.3f}\n"
            f"4. α_max = arcsin({NA:.3f}) = {alpha_max:.1f}°\n\n"
            f"✅ **Ответ:** α_max = {alpha_max:.1f}°"
        )
        
        return task, solution
    
    # ============= КВАНТОВАЯ ФИЗИКА =============
    
    def quantum_photoeffect(self):
        """Фотоэффект"""
        nu = random.randint(6, 15) * 10**14
        A = round(random.uniform(2.0, 4.0), 1)
        h = 4.14 * 10**-15
        E = h * nu
        Ek = max(0, E - A)
        
        task = (f"📸 На металл падает свет частотой {nu/10**14:.1f}·10¹⁴ Гц. "
                f"Работа выхода электронов {A} эВ. "
                f"Найти максимальную кинетическую энергию фотоэлектронов.")
        
        solution = (
            f"📌 **Формула:** hν = A + E_k  →  E_k = hν - A\n\n"
            f"📊 **Подстановка:**\n"
            f"• ν = {nu/10**14:.1f}·10¹⁴ Гц\n"
            f"• A = {A} эВ\n"
            f"• h = 4.14·10⁻¹⁵ эВ·с\n\n"
            f"📝 **Решение:**\n"
            f"1. Энергия фотона: E_ф = hν = 4.14·10⁻¹⁵ × {nu/10**14:.1f}·10¹⁴ = {E:.2f} эВ\n"
            f"2. Кинетическая энергия: E_k = E_ф - A = {E:.2f} - {A} = {Ek:.2f} эВ\n\n"
            f"✅ **Ответ:** E_k = {Ek:.2f} эВ"
        )
        
        return task, solution
    
    def quantum_spectrum(self):
        """Спектр водорода"""
        n1 = random.randint(1, 3)
        n2 = n1 + random.randint(1, 3)
        R = 13.6
        dE = R * abs(1/n1**2 - 1/n2**2)
        lam = 1240 / dE
        
        task = (f"⚛️ В атоме водорода электрон переходит с уровня n = {n2} "
                f"на уровень n = {n1}. Найти длину волны излучения.")
        
        solution = (
            f"📌 **Формула:** ΔE = 13.6·(1/n₁² - 1/n₂²), λ = 1240/ΔE (нм)\n\n"
            f"📊 **Подстановка:**\n"
            f"• n₁ = {n1}\n"
            f"• n₂ = {n2}\n\n"
            f"📝 **Решение:**\n"
            f"1. Энергия перехода: ΔE = 13.6 × (1/{n1}² - 1/{n2}²)\n"
            f"2. 1/{n1}² = {1/n1**2:.3f}, 1/{n2}² = {1/n2**2:.3f}\n"
            f"3. ΔE = 13.6 × ({1/n1**2:.3f} - {1/n2**2:.3f}) = {dE:.2f} эВ\n"
            f"4. Длина волны: λ = 1240 / {dE:.2f} = {lam:.0f} нм\n\n"
            f"✅ **Ответ:** λ = {lam:.0f} нм"
        )
        
        return task, solution
    
    def quantum_bohr(self):
        """Радиус Бора"""
        n = random.randint(1, 5)
        a0 = 0.053
        r = a0 * n**2
        
        task = (f"⚛️ Найти радиус n = {n} орбиты электрона в атоме водорода (в нм).")
        
        solution = (
            f"📌 **Формула:** r_n = a₀·n², a₀ = 0.053 нм\n\n"
            f"📊 **Подстановка:**\n"
            f"• n = {n}\n"
            f"• a₀ = 0.053 нм\n\n"
            f"📝 **Решение:**\n"
            f"1. Радиус n-й орбиты: r_n = a₀·n²\n"
            f"2. r = 0.053 × {n}² = {r:.3f} нм\n\n"
            f"✅ **Ответ:** r = {r:.3f} нм"
        )
        
        return task, solution
    
    def quantum_debroglie(self):
        """Волна де Бройля"""
        v = random.randint(1, 8) * 10**6
        m = 9.11 * 10**-31
        h = 6.63 * 10**-34
        lam = h / (m * v)
        
        task = (f"🌊 Электрон движется со скоростью {v/10**6:.0f}·10⁶ м/с. "
                f"Найти длину волны де Бройля.")
        
        solution = (
            f"📌 **Формула:** λ = h/(mv)\n\n"
            f"📊 **Подстановка:**\n"
            f"• h = 6.63·10⁻³⁴ Дж·с\n"
            f"• m = 9.11·10⁻³¹ кг\n"
            f"• v = {v/10**6:.0f}·10⁶ м/с\n\n"
            f"📝 **Решение:**\n"
            f"1. λ = h/(mv) = 6.63·10⁻³⁴ / (9.11·10⁻³¹ × {v/10**6:.0f}·10⁶)\n"
            f"2. λ = {lam:.2e} м\n"
            f"3. Переводим в нанометры: {lam*10**9:.3f} нм\n\n"
            f"✅ **Ответ:** λ = {lam*10**9:.3f} нм"
        )
        
        return task, solution
    
    def quantum_photon(self):
        """Энергия фотона"""
        lam = random.randint(400, 700)
        E = 1240 / lam
        
        task = (f"💡 Фотон имеет длину волны {lam} нм. "
                f"Найти энергию фотона в электрон-вольтах.")
        
        solution = (
            f"📌 **Формула:** E = hc/λ = 1240/λ (эВ, λ в нм)\n\n"
            f"📊 **Подстановка:**\n"
            f"• λ = {lam} нм\n\n"
            f"📝 **Решение:**\n"
            f"1. Энергия фотона: E = 1240 / λ\n"
            f"2. E = 1240 / {lam} = {E:.1f} эВ\n\n"
            f"✅ **Ответ:** E = {E:.1f} эВ"
        )
        
        return task, solution
    
    def quantum_uncertainty(self):
        """Соотношение неопределённостей"""
        dx = round(random.uniform(0.5, 2.0), 1) * 10**-10
        h_bar = 1.05 * 10**-34
        dp_min = h_bar / (2 * dx)
        
        task = (f"❓ Неопределённость координаты электрона Δx = {dx*10**10:.1f} Å. "
                f"Найти минимальную неопределённость импульса.")
        
        solution = (
            f"📌 **Формула:** Δx·Δp ≥ ħ/2\n\n"
            f"📊 **Подстановка:**\n"
            f"• Δx = {dx:.1e} м\n"
            f"• ħ = 1.05·10⁻³⁴ Дж·с\n\n"
            f"📝 **Решение:**\n"
            f"1. Соотношение неопределённостей Гейзенберга: Δx·Δp ≥ ħ/2\n"
            f"2. Минимальное Δp: Δp_min = ħ/(2Δx)\n"
            f"3. Δp_min = 1.05·10⁻³⁴ / (2 × {dx:.1e}) = {dp_min:.2e} кг·м/с\n\n"
            f"✅ **Ответ:** Δp_min = {dp_min:.2e} кг·м/с"
        )
        
        return task, solution
    
    def quantum_decay(self):
        """Радиоактивный распад"""
        T = random.randint(5, 30)
        t = T * random.randint(2, 4)
        N0 = 1000
        N = N0 / (2**(t/T))
        
        task = (f"☢️ Период полураспада изотопа {T} минут. "
                f"Сколько ядер останется из {N0} через {t} минут?")
        
        solution = (
            f"📌 **Формула:** N = N₀·2^(-t/T)\n\n"
            f"📊 **Подстановка:**\n"
            f"• N₀ = {N0}\n"
            f"• t = {t} мин\n"
            f"• T = {T} мин\n\n"
            f"📝 **Решение:**\n"
            f"1. Число периодов полураспада: n = t/T = {t}/{T} = {t/T}\n"
            f"2. N = {N0} / 2^{t/T} = {N0} / {2**(t/T):.0f} = {N:.0f}\n\n"
            f"✅ **Ответ:** останется примерно {N:.0f} ядер"
        )
        
        return task, solution
    
    def quantum_mass_defect(self):
        """Дефект массы"""
        dm = round(random.uniform(0.01, 0.05), 3)
        E = dm * 931.5
        
        task = (f"⚛️ Дефект массы ядра составляет {dm} а.е.м. "
                f"Найти энергию связи в МэВ.")
        
        solution = (
            f"📌 **Формула:** E_св = Δm·c² = Δm·931.5 МэВ\n\n"
            f"📊 **Подстановка:**\n"
            f"• Δm = {dm} а.е.м.\n\n"
            f"📝 **Решение:**\n"
            f"1. Энергия связи: E_св = Δm·c²\n"
            f"2. 1 а.е.м. соответствует 931.5 МэВ\n"
            f"3. E = {dm} × 931.5 = {E:.1f} МэВ\n\n"
            f"✅ **Ответ:** E_св = {E:.1f} МэВ"
        )
        
        return task, solution
    
    def quantum_compton(self):
        """Комптон-эффект"""
        task = "💥 В чём суть комптоновского рассеяния?"
        
        solution = (
            f"📌 **Явление:** Комптон-эффект\n\n"
            f"📝 **Объяснение:**\n"
            f"1. Комптоновское рассеяние - это упругое рассеяние фотона на свободном электроне\n"
            f"2. Фотон передаёт электрону часть своей энергии и импульса\n"
            f"3. В результате длина волны рассеянного фотона увеличивается\n"
            f"4. Изменение длины волны зависит от угла рассеяния: Δλ = (h/(mₑc))·(1 - cos θ)\n"
            f"5. Этот эффект доказывает корпускулярную природу света\n\n"
            f"✅ **Вывод:** Фотон ведёт себя как частица, передавая энергию и импульс электрону"
        )
        
        return task, solution
    
    def quantum_alpha(self):
        """Альфа-распад"""
        task = "☢️ Написать реакцию α-распада радия-226."
        
        solution = (
            f"📌 **Реакция:** ²²⁶Ra → ²²²Rn + α\n\n"
            f"📝 **Объяснение:**\n"
            f"1. При α-распаде ядро испускает α-частицу (ядро гелия-4)\n"
            f"2. Массовое число уменьшается на 4, зарядовое - на 2\n"
            f"3. Радий-226 (Z=88) → Радон-222 (Z=86) + Гелий-4 (Z=2)\n\n"
            f"✅ **Ответ:** ²²⁶Ra → ²²²Rn + ⁴He"
        )
        
        return task, solution
    
    def quantum_dual(self):
        """Корпускулярно-волновой дуализм"""
        task = "🌀 Что такое корпускулярно-волновой дуализм?"
        
        solution = (
            f"📌 **Определение:** Корпускулярно-волновой дуализм - свойство микрообъектов проявлять одновременно свойства частиц и волн\n\n"
            f"📝 **Объяснение:**\n"
            f"1. Частицы (электроны, протоны и др.) могут проявлять волновые свойства\n"
            f"2. Волны (свет) могут проявлять свойства частиц (фотонов)\n"
            f"3. Связь между корпускулярными и волновыми характеристиками:\n"
            f"   • E = hν (энергия связана с частотой)\n"
            f"   • p = h/λ (импульс связан с длиной волны)\n"
            f"4. Это фундаментальное свойство квантовой физики\n\n"
            f"✅ **Вывод:** Микрообъекты имеют двойственную природу"
        )
        
        return task, solution
    
    def quantum_wien(self):
        """Закон смещения Вина"""
        T = random.randint(2000, 6000)
        lam_max = 2.9 * 10**6 / T
        
        task = (f"🌡️ Температура абсолютно чёрного тела {T} К. "
                f"Найти длину волны, на которую приходится максимум излучения.")
        
        solution = (
            f"📌 **Формула:** λ_max·T = b, b = 2.9·10⁶ нм·К\n\n"
            f"📊 **Подстановка:**\n"
            f"• T = {T} К\n"
            f"• b = 2.9·10⁶ нм·К\n\n"
            f"📝 **Решение:**\n"
            f"1. Закон смещения Вина: λ_max·T = b\n"
            f"2. λ_max = b/T = 2.9·10⁶ / {T}\n"
            f"3. λ_max = {lam_max:.0f} нм\n\n"
            f"✅ **Ответ:** λ_max = {lam_max:.0f} нм"
        )
        
        return task, solution

# Класс для управления пользователями
class UserManager:
    def __init__(self):
        self.users: Dict[int, dict] = {}
        self.rate_limits: Dict[int, List[datetime]] = defaultdict(list)
    
    def get_user(self, user_id: int) -> dict:
        """Получение данных пользователя"""
        if user_id not in self.users:
            self.users[user_id] = {
                "solved_tasks": [],
                "favorite_tasks": [],
                "last_activity": datetime.now(),
                "daily_count": 0,
                "device_type": "desktop",
                "stats": {
                    "total_solved": 0,
                    "sections_completed": defaultdict(int)
                }
            }
        return self.users[user_id]
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Проверка лимита запросов"""
        now = datetime.now()
        user_requests = self.rate_limits[user_id]
        
        # Очищаем старые запросы
        user_requests = [req for req in user_requests if now - req < timedelta(minutes=1)]
        self.rate_limits[user_id] = user_requests
        
        return len(user_requests) < 5
    
    def update_activity(self, user_id: int):
        """Обновление активности пользователя"""
        user = self.get_user(user_id)
        user["last_activity"] = datetime.now()
    
    def detect_device(self, message: Message) -> str:
        """Определение типа устройства"""
        if message.text and len(message.text) < 50:
            return "mobile"
        return "desktop"

# Инициализация
task_generator = TaskGenerator()
user_manager = UserManager()

# Функции для создания клавиатур
def get_main_keyboard(device_type: str = "desktop") -> InlineKeyboardMarkup:
    """Главное меню"""
    buttons = []
    
    if device_type == "mobile":
        for key, name in SECTIONS.items():
            buttons.append([InlineKeyboardButton(text=name, callback_data=f"sec_{key}")])
    else:
        sections_list = list(SECTIONS.items())
        for i in range(0, len(sections_list), 2):
            row = []
            for j in range(2):
                if i + j < len(sections_list):
                    key, name = sections_list[i + j]
                    row.append(InlineKeyboardButton(text=name, callback_data=f"sec_{key}"))
            buttons.append(row)
    
    buttons.extend([
        [InlineKeyboardButton(text="🎲 Случайная задача", callback_data="sec_random")],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
            InlineKeyboardButton(text="❓ Помощь", callback_data="help")
        ]
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_task_keyboard(section: str) -> InlineKeyboardMarkup:
    """Клавиатура для задачи"""
    buttons = [
        [InlineKeyboardButton(text="📖 Показать решение", callback_data="show_sol")],
        [
            InlineKeyboardButton(text="🔄 Ещё задачу", callback_data=f"sec_{section}"),
            InlineKeyboardButton(text="📚 Другая тема", callback_data="back_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Обработчики команд
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    user = user_manager.get_user(user_id)
    device = user_manager.detect_device(message)
    user["device_type"] = device
    
    welcome_text = [
        f"{hbold('👋 Привет, ' + (message.from_user.first_name or 'друг') + '!')}",
        "",
        "Я бот для изучения физики. Здесь ты найдёшь:",
        "✅ 60+ задач по разным темам",
        "✅ Подробные решения с формулами",
        "✅ Пошаговые объяснения",
        "",
        "📚 **Доступные разделы:**"
    ]
    
    for name in SECTIONS.values():
        welcome_text.append(f"• {name}")
    
    welcome_text.append("\n👇 Выбери раздел для начала!")
    
    await message.answer(
        "\n".join(welcome_text),
        reply_markup=get_main_keyboard(device),
        parse_mode="HTML"
    )
    
    logger.info(f"User {user_id} started the bot")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = [
        f"{hbold('🔍 СПРАВКА ПО БОТУ')}",
        "",
        "**Как пользоваться:**",
        "1️⃣ Выбери раздел физики",
        "2️⃣ Получи случайную задачу",
        "3️⃣ Попробуй решить самостоятельно",
        "4️⃣ Посмотри подробное решение",
        "",
        "**Команды:**",
        "• /start - Начать работу",
        "• /help - Показать эту справку"
    ]
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ В меню", callback_data="back_menu")]
    ])
    
    await message.answer("\n".join(help_text), reply_markup=kb, parse_mode="HTML")

# Обработчики callback-запросов
@dp.callback_query(lambda c: c.data.startswith("sec_"))
async def process_section(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора раздела"""
    user_id = callback.from_user.id
    user = user_manager.get_user(user_id)
    
    if not user_manager.check_rate_limit(user_id):
        await callback.answer("⏳ Слишком много запросов! Подождите минуту.", show_alert=True)
        return
    
    sec = callback.data.replace("sec_", "")
    
    if sec == "random":
        sec = random.choice(list(task_generator.generators.keys()))
        header = f"🎲 Случайная задача ({SECTIONS[sec]})"
    else:
        header = SECTIONS[sec]
    
    try:
        # Получаем случайную задачу
        generator = random.choice(task_generator.generators[sec])
        task, solution = generator()
        
        # Сохраняем в состояние
        await state.update_data(
            task_text=task,
            solution_text=solution,
            section=sec
        )
        
        # Обновляем статистику
        user["stats"]["sections_completed"][sec] += 1
        user["stats"]["total_solved"] += 1
        
        task_message = [
            f"{hbold(header)}",
            "",
            f"{hbold('📌 ЗАДАЧА:')}",
            task,
            "",
            "💡 _Нажми кнопку, чтобы увидеть решение!_"
        ]
        
        await callback.message.edit_text(
            "\n".join(task_message),
            reply_markup=get_task_keyboard(sec),
            parse_mode="HTML"
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.message.edit_text(
            "❌ Ошибка. Попробуйте другой раздел.",
            reply_markup=get_main_keyboard(user["device_type"])
        )
        await callback.answer("Ошибка!", show_alert=True)

@dp.callback_query(lambda c: c.data == "show_sol")
async def show_solution(callback: CallbackQuery, state: FSMContext):
    """Показать решение"""
    data = await state.get_data()
    solution = data.get("solution_text", "Решение не найдено")
    section = data.get("section", "mechanics")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Ещё задачу", callback_data=f"sec_{section}")],
        [InlineKeyboardButton(text="📚 В меню", callback_data="back_menu")]
    ])
    
    await callback.message.answer(solution, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в меню"""
    user_id = callback.from_user.id
    user = user_manager.get_user(user_id)
    
    await state.clear()
    
    await callback.message.edit_text(
        f"{hbold('📚 ГЛАВНОЕ МЕНЮ')}\n\nВыберите раздел физики:",
        reply_markup=get_main_keyboard(user["device_type"]),
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "stats")
async def show_stats(callback: CallbackQuery):
    """Показать статистику"""
    user_id = callback.from_user.id
    user = user_manager.get_user(user_id)
    
    stats_text = [
        f"{hbold('📊 ВАША СТАТИСТИКА')}",
        "",
        f"✅ Всего решено: {user['stats']['total_solved']}",
        "",
        "**По разделам:**"
    ]
    
    for section, count in user['stats']['sections_completed'].items():
        section_name = SECTIONS.get(section, section)
        stats_text.append(f"• {section_name}: {count}")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_menu")]
    ])
    
    await callback.message.edit_text(
        "\n".join(stats_text),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback: CallbackQuery):
    """Показать справку"""
    help_text = [
        f"{hbold('🔍 СПРАВКА')}",
        "",
        "1. Выбери раздел в меню",
        "2. Реши задачу самостоятельно",
        "3. Нажми 'Показать решение'",
        "4. Сравни со своим ответом",
        "",
        "Статистика сохраняется автоматически!"
    ]
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_menu")]
    ])
    
    await callback.message.edit_text(
        "\n".join(help_text),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()

# Запуск бота
# ===== НОВЫЙ КОД ДЛЯ PYTHONANYWHERE =====
# Запуск бота
# ===== НОВЫЙ КОД ДЛЯ PYTHONANYWHERE =====
# Запуск бота
if __name__ == "__main__":
    print("Бот запускается...")
    asyncio.run(dp.start_polling(bot))