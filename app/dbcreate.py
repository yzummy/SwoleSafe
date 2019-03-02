from main import db, User, BodyPart, Exercise

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    bp1 = BodyPart(name="chest")
    bp2 = BodyPart(name="bicep")
    bp3 = BodyPart(name='quadriceps')
    bp4 = BodyPart(name='hamstring')
    bp5 = BodyPart(name='deltoids')
    db.session.add_all([bp1, bp2, bp3, bp4, bp5])

    e1 = Exercise(name="Bicep Curl", description="Contract bicep while holding weight then release slowly")
    e1.uses.append(bp2)

    e2 = Exercise(name="Front Raise", description="Raise dumbells in front of you")
    e2.uses.append(bp5)

    e3 = Exercise(name="Squat", description="Pretend like you are sitting down and getting up from an invisible chair")
    e3.uses.extend([bp3, bp4])


    db.session.add_all([e1, e2, e3])

    u1 = User(username="ArnoldSchwazzaneger123", password="abc", level="advanced")
    u1.targets.append(bp5)

    u2 = User(username="DwanedaRockJohnson", password="123", level="beginner")
    u2.targets.extend([bp2, bp3])

    db.session.add_all([u1, u2])


    db.session.commit()
