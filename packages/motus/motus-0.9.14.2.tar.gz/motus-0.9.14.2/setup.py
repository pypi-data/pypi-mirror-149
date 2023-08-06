from setuptools import setup

setup(
    name='motus',
    version='0.9.14.2',
    description='Paquetería para el Análisis Conductual de Patrones de Desplazamiento',
    author='Escamilla, Toledo, Tamayo, Avendanio, Leon, Eslava, Hernandez',
    author_email='escamilla.een@gmail.com',
    packages=['motus', 'motus.entropia_divergencia', 'motus.fisica_estadistica', 'motus.graficador',
              'motus.regiones_cuadriculadas', 'motus.regresion_lineal', 'motus.rutas_distancias'],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'sklearn'
    ],
)