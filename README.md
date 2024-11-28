# Cosmic Garden 🌱🚀

A space-themed gardening simulation game where players can grow and maintain plants across different planets in our solar system.

## Features

- 🌍 Multiple planets with unique environments
- 🌱 Various plant species adapted to space conditions
- 💰 In-game economy with cosmic credits
- 📈 Experience and leveling system
- 🏆 Achievements and challenges

## Technical Stack
- Backend: Python/Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Authentication: Flask-Login
- Environment Management: python-dotenv

## Project Structure
```
/CosmicGarden
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── static/            # Static assets (CSS, JS, images)
├── templates/         # HTML templates
└── instance/          # Instance-specific files
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following content:
```
SECRET_KEY=your-secret-key-here
```

4. Initialize the database:
```bash
python app.py
```

5. Access the application:
- Open your browser and go to `http://localhost:5000`
- Create an account or log in
- Start your cosmic gardening adventure!

## Game Features

### Planet Environments

#### Mars
- Low gravity (0.38g)
- Cold desert climate
- Thin CO2 atmosphere
- Perfect for hardy, low-maintenance plants

#### Venus Garden Dome
- Near Earth gravity (0.9g)
- Controlled tropical environment
- Protected from harsh surface conditions
- Ideal for exotic, heat-loving plants

#### Europa Station
- Very low gravity (0.134g)
- Ice-cold environment
- Artificial atmosphere
- Specialized for cold-resistant plants

### Plant Species
- Cosmic Cactus
   - Thrives in low gravity
   - Minimal water requirements
   - Common rarity

- Stellar Sunflower
   - Tracks distant suns
   - Moderate care needs
   - Uncommon rarity

- Gravity Grass
   - Grows toward gravity sources
   - Easy to maintain
   - Common rarity

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Guidelines
- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Add comments for complex logic
- Update documentation for new features

## Future Enhancements
- [ ] Multiplayer features
- [ ] More planets and environments
- [ ] Trading system between players
- [ ] Advanced plant breeding mechanics
- [ ] Weather system simulation

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- GitHub: [@KisnaIsOP](https://github.com/KisnaIsOP)
- Project Link: [https://github.com/KisnaIsOP/CosmicGarden](https://github.com/KisnaIsOP/CosmicGarden)
