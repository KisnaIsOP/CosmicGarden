from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import random
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cosmic_garden.db'
db = SQLAlchemy(app)

# Models
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.Float, nullable=False)
    atmosphere = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    gardens = db.relationship('Garden', backref='planet', lazy=True)

class Garden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    size = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_tended = db.Column(db.DateTime, default=datetime.utcnow)
    plants = db.relationship('Plant', backref='garden', lazy=True)

class PlantSpecies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    growth_time = db.Column(db.Integer, nullable=False)  # in hours
    required_gravity = db.Column(db.Float, nullable=False)
    required_atmosphere = db.Column(db.String(50), nullable=False)
    experience_reward = db.Column(db.Integer, nullable=False)
    rarity = db.Column(db.String(20), nullable=False)
    ascii_art = db.Column(db.String(500), nullable=False)  # ASCII art for different growth stages
    special_traits = db.Column(db.String, default='[]')  # JSON string of special abilities
    plants = db.relationship('Plant', backref='species', lazy=True)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey('plant_species.id'), nullable=False)
    garden_id = db.Column(db.Integer, db.ForeignKey('garden.id'), nullable=False)
    planted_at = db.Column(db.DateTime, default=datetime.utcnow)
    growth_stage = db.Column(db.Integer, default=0)  # 0:Seed, 1:Sprout, 2:Young, 3:Mature, 4:Flowering
    health = db.Column(db.Integer, default=100)
    last_watered = db.Column(db.DateTime, default=datetime.utcnow)
    is_mature = db.Column(db.Boolean, default=False)
    oxygen_production = db.Column(db.Float, default=0)  # Oxygen produced per hour
    energy_consumption = db.Column(db.Float, default=0)  # Energy consumed per hour
    mutation_level = db.Column(db.Integer, default=0)  # 0-5, affects appearance and production
    achievements = db.Column(db.String, default='[]')  # JSON string of achieved milestones
    resources_produced = db.Column(db.String, default='{}')  # JSON string of resources
    affected_by_events = db.Column(db.String, default='[]')  # JSON string of active events

    def get_growth_symbol(self):
        symbols = ['🌱', '🌿', '🌵', '🌸', '🌺']  # Can be replaced with ASCII art
        return symbols[min(self.growth_stage, 4)]

    def get_health_status(self):
        if self.health >= 80:
            return 'Thriving', '💚'
        elif self.health >= 60:
            return 'Healthy', '💛'
        elif self.health >= 40:
            return 'Stressed', '🟧'
        elif self.health >= 20:
            return 'Critical', '❤️'
        return 'Dying', '💔'

    def update_growth(self):
        current_time = datetime.utcnow()
        hours_since_planted = (current_time - self.planted_at).total_seconds() / 3600
        species = PlantSpecies.query.get(self.species_id)
        garden = Garden.query.get(self.garden_id)
        planet = Planet.query.get(garden.planet_id)
        
        # Basic growth calculation
        expected_stage = min(4, int(hours_since_planted / species.growth_time * 4))
        
        # Environmental factors
        gravity_effect = 1 - abs(species.required_gravity - planet.gravity) * 0.5
        atmosphere_match = species.required_atmosphere == planet.atmosphere
        environment_multiplier = gravity_effect * (1.2 if atmosphere_match else 0.8)
        
        # Apply environmental effects
        self.growth_stage = min(4, int(expected_stage * environment_multiplier))
        self.is_mature = self.growth_stage >= 3
        
        # Update resources
        if self.is_mature:
            self.oxygen_production = species.experience_reward * environment_multiplier * 0.1
            resources = json.loads(self.resources_produced)
            if self.growth_stage == 4:  # Flowering stage
                resources['seeds'] = resources.get('seeds', 0) + 1
            self.resources_produced = json.dumps(resources)
        
        # Random mutations based on environment
        if random.random() < 0.05 * abs(1 - environment_multiplier):
            self.mutation_level = min(5, self.mutation_level + 1)

# Initialize sample data
def init_sample_data():
    # Create planets if they don't exist
    if not Planet.query.first():
        planets = [
            {
                'name': 'Mars',
                'climate': 'Cold Desert',
                'gravity': 0.38,
                'atmosphere': 'Thin CO2',
                'difficulty': 3,
                'description': 'The Red Planet challenges gardeners with its harsh conditions.',
                'temperature': 20.0
            },
            {
                'name': 'Venus Garden Dome',
                'climate': 'Controlled Tropical',
                'gravity': 0.9,
                'atmosphere': 'Filtered Toxic',
                'difficulty': 4,
                'description': 'Special domes protect your garden from Venus\'s extreme environment.',
                'temperature': 30.0
            },
            {
                'name': 'Europa Station',
                'climate': 'Ice Cold',
                'gravity': 0.134,
                'atmosphere': 'Artificial',
                'difficulty': 5,
                'description': 'An icy moon of Jupiter with underground oceans.',
                'temperature': -10.0
            }
        ]
        for planet_data in planets:
            planet = Planet(**planet_data)
            db.session.add(planet)

    # Create plant species if they don't exist
    if not PlantSpecies.query.first():
        species = [
            {
                'name': 'Cosmic Cactus',
                'description': 'A hardy plant that thrives in low gravity.',
                'growth_time': 24,
                'required_gravity': 0.3,
                'required_atmosphere': 'Any',
                'experience_reward': 50,
                'rarity': 'Common',
                'ascii_art': '''
                    Stage 0: .
                    Stage 1: |
                    Stage 2: Y
                    Stage 3: ¥
                    Stage 4: Ψ
                ''',
                'special_traits': json.dumps(['drought_resistant', 'low_gravity_adapted'])
            },
            {
                'name': 'Stellar Sunflower',
                'description': 'A beautiful flower that tracks distant suns.',
                'growth_time': 48,
                'required_gravity': 0.5,
                'required_atmosphere': 'Thin',
                'experience_reward': 100,
                'rarity': 'Uncommon',
                'ascii_art': '''
                    Stage 0: .
                    Stage 1: i
                    Stage 2: ⚘
                    Stage 3: ❀
                    Stage 4: ✿
                ''',
                'special_traits': json.dumps(['light_seeking', 'energy_producing'])
            },
            {
                'name': 'Gravity Grass',
                'description': 'Grass that grows towards gravity sources.',
                'growth_time': 12,
                'required_gravity': 0.1,
                'required_atmosphere': 'Any',
                'experience_reward': 30,
                'rarity': 'Common',
                'ascii_art': '''
                    Stage 0: .
                    Stage 1: ,
                    Stage 2: ^^
                    Stage 3: ^^^
                    Stage 4: ^^^^
                ''',
                'special_traits': json.dumps(['fast_growing', 'soil_stabilizing'])
            },
            {
                'name': 'Void Vine',
                'description': 'A mysterious vine that thrives in zero gravity.',
                'growth_time': 36,
                'required_gravity': 0.0,
                'required_atmosphere': 'Thin',
                'experience_reward': 80,
                'rarity': 'Rare',
                'ascii_art': '''
                    Stage 0: .
                    Stage 1: ~
                    Stage 2: ≈
                    Stage 3: ≋
                    Stage 4: ⋋
                ''',
                'special_traits': json.dumps(['zero_gravity_growth', 'rapid_mutation'])
            }
        ]
        for species_data in species:
            plant_species = PlantSpecies(**species_data)
            db.session.add(plant_species)

    db.session.commit()

# Template filters
@app.template_filter('from_json')
def from_json_filter(value):
    return json.loads(value) if value else {}

# Routes
@app.route('/')
def index():
    gardens = Garden.query.all()
    planets = Planet.query.all()
    return render_template('index.html', gardens=gardens, planets=planets)

@app.route('/garden/<int:garden_id>')
def view_garden(garden_id):
    garden = Garden.query.get_or_404(garden_id)
    plants = Plant.query.filter_by(garden_id=garden_id).all()
    plant_species = PlantSpecies.query.all()
    planet = Planet.query.get(garden.planet_id)
    
    # Update plant growth and generate random events
    current_time = datetime.utcnow()
    events = []
    
    for plant in plants:
        # Update plant growth
        plant.update_growth()
        
        # Random events
        if random.random() < 0.1:  # 10% chance of event
            event_types = [
                {
                    'name': 'Solar Flare',
                    'description': 'A sudden burst of solar radiation!',
                    'effects': 'Plants may experience stress.'
                },
                {
                    'name': 'Cosmic Rain',
                    'description': 'Strange particles are falling from space.',
                    'effects': 'Increased mutation chance.'
                },
                {
                    'name': 'Gravity Fluctuation',
                    'description': 'Local gravity is unstable.',
                    'effects': 'Plant growth may be affected.'
                }
            ]
            events.append(random.choice(event_types))
    
    db.session.commit()
    
    return render_template('garden.html', 
                         garden=garden, 
                         plants=plants, 
                         plant_species=plant_species,
                         planet=planet,
                         random_events=events,
                         now=current_time)

@app.route('/garden/create', methods=['POST'])
def create_garden():
    name = request.form.get('name')
    planet_id = request.form.get('planet_id')
    
    if name and planet_id:
        garden = Garden(name=name, planet_id=planet_id)
        db.session.add(garden)
        db.session.commit()
        flash('Garden created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/plant/<int:plant_id>/water', methods=['POST'])
def water_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    current_time = datetime.utcnow()
    
    # Check if enough time has passed since last watering
    if (current_time - plant.last_watered).total_seconds() >= 3600:  # 1 hour
        plant.last_watered = current_time
        plant.health = min(100, plant.health + 20)
        
        # Chance of mutation when watering
        if random.random() < 0.05:  # 5% chance
            plant.mutation_level = min(5, plant.mutation_level + 1)
        
        db.session.commit()
        flash('Plant watered successfully!', 'success')
    else:
        flash('Plant was watered recently. Please wait before watering again.', 'warning')
    
    return redirect(url_for('view_garden', garden_id=plant.garden_id))

@app.route('/plant/<int:plant_id>/harvest', methods=['POST'])
def harvest_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.growth_stage >= 4:  # Only harvest mature plants
        # Get resources
        resources = json.loads(plant.resources_produced)
        seeds = resources.get('seeds', 0)
        
        # Create achievement for first harvest
        achievements = json.loads(plant.achievements)
        if 'first_harvest' not in achievements:
            achievements.append('first_harvest')
            plant.achievements = json.dumps(achievements)
        
        # Reset plant to seedling stage with some benefits
        plant.growth_stage = 0
        plant.health = 100
        plant.last_watered = datetime.utcnow()
        plant.resources_produced = json.dumps({'seeds': 0})
        
        flash(f'Plant harvested successfully! Collected {seeds} seeds.', 'success')
        db.session.commit()
    else:
        flash('Plant is not ready for harvest yet.', 'warning')
    
    return redirect(url_for('view_garden', garden_id=plant.garden_id))

@app.route('/garden/<int:garden_id>/add_plant', methods=['POST'])
def add_plant(garden_id):
    species_id = request.form.get('species_id', type=int)
    if not species_id:
        flash('Please select a plant species.', 'error')
        return redirect(url_for('view_garden', garden_id=garden_id))
    
    # Create new plant
    new_plant = Plant(
        species_id=species_id,
        garden_id=garden_id,
        planted_at=datetime.utcnow(),
        last_watered=datetime.utcnow()
    )
    
    db.session.add(new_plant)
    db.session.commit()
    
    flash('New plant added to your garden!', 'success')
    return redirect(url_for('view_garden', garden_id=garden_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(debug=True)
