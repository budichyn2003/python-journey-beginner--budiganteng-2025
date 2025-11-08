import click
from password_generator import PasswordGenerator
from password_validator import PasswordValidator

@click.group()
def cli():
    """CLI Password Generator dan Validator"""
    pass

@cli.command()
@click.option('--length', '-l', default=12, help='Panjang password')
@click.option('--no-lower', is_flag=True, help='Tanpa huruf kecil')
@click.option('--no-upper', is_flag=True, help='Tanpa huruf besar')
@click.option('--no-digits', is_flag=True, help='Tanpa angka')
@click.option('--no-symbols', is_flag=True, help='Tanpa simbol')
@click.option('--min-each', default=1, help='Jumlah minimal setiap jenis karakter')
def generate(length, no_lower, no_upper, no_digits, no_symbols, min_each):
    """Generate password acak"""
    generator = PasswordGenerator()
    try:
        result = generator.generate_password(
            length=length,
            use_lower=not no_lower,
            use_upper=not no_upper,
            use_digits=not no_digits,
            use_symbols=not no_symbols,
            min_each=min_each
        )
        password = result['password']
        strength = result['strength']
        
        click.echo("\nPassword yang dihasilkan:")
        click.echo(f"\n{password}\n")
        click.echo(f"Skor Kekuatan: {strength['score']}/100")
        click.echo(f"Kategori: {strength['strength']}")
        if strength['feedback']:
            click.echo("\nSaran:")
            for feedback in strength['feedback']:
                click.echo(f"- {feedback}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--words', '-w', default=3, help='Jumlah kata')
@click.option('--no-number', is_flag=True, help='Tanpa angka')
@click.option('--no-symbol', is_flag=True, help='Tanpa simbol')
def memorable(words, no_number, no_symbol):
    """Generate password yang mudah diingat"""
    generator = PasswordGenerator()
    result = generator.generate_memorable_password(
        num_words=words,
        add_number=not no_number,
        add_symbol=not no_symbol
    )
    password = result['password']
    strength = result['strength']
    
    click.echo("\nPassword yang mudah diingat:")
    click.echo(f"\n{password}\n")
    click.echo(f"Skor Kekuatan: {strength['score']}/100")
    click.echo(f"Kategori: {strength['strength']}")
    if strength['feedback']:
        click.echo("\nSaran:")
        for feedback in strength['feedback']:
            click.echo(f"- {feedback}")

@cli.command()
@click.option('--length', '-l', default=6, help='Panjang PIN')
def pin(length):
    """Generate PIN numerik"""
    generator = PasswordGenerator()
    try:
        pin = generator.generate_pin(length)
        click.echo(f"\nPIN yang dihasilkan: {pin}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('password')
def validate(password):
    """Validasi kekuatan password"""
    validator = PasswordValidator()
    try:
        # Validasi kriteria dasar
        validator.validate_password(password)
        
        # Hitung dan tampilkan skor
        result = validator.calculate_strength(password)
        
        click.echo(f"\nSkor Kekuatan: {result['score']}/100")
        click.echo(f"Kategori: {result['strength']}")
        
        if result['feedback']:
            click.echo("\nSaran untuk meningkatkan kekuatan:")
            for feedback in result['feedback']:
                click.echo(f"- {feedback}")
                
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def history():
    """Tampilkan history password yang telah di-generate"""
    generator = PasswordGenerator()
    history = generator.get_history()
    
    if not history:
        click.echo("Belum ada password yang di-generate.")
        return
        
    click.echo("\nHistory Password:")
    for idx, entry in enumerate(history, 1):
        click.echo(f"\n{idx}. Generated at: {entry['timestamp']}")
        click.echo(f"   Password: {entry['password']}")
        click.echo(f"   Strength: {entry['strength']['strength']} ({entry['strength']['score']}/100)")

if __name__ == '__main__':
    cli()