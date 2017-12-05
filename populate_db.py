from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Item, Category


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

firstUser = User(name="Ziggy Stardust", email="garb@aol.com", picture="https://upload.wikimedia.org/wikipedia/commons/1/1e/David-Bowie_Early.jpg")
session.add(firstUser)
session.commit()

firstCat = Category(name="Thelonious Monk", user_id=firstUser.id)
session.add(firstCat)
session.commit()

item1 = Item(name='Solo Monk', year=1965, icon='https://upload.wikimedia.org/wikipedia/en/2/21/Solo_Monk.jpg', description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eget quam non nulla sodales laoreet. Etiam nec ipsum ac velit laoreet sodales. Sed efficitur hendrerit risus ut suscipit. Morbi vel nulla in urna cursus varius. Curabitur facilisis, tellus ut scelerisque mollis, est augue lacinia lorem, at imperdiet urna tortor ac felis. Etiam efficitur quam eget felis lacinia, eu pretium ligula maximus. Donec est ex, molestie quis ultrices sed, hendrerit id nibh.", category_id=firstCat.id, user_id=firstUser.id)
session.add(item1)
session.commit()

item5 = Item(name='Brilliant Corners', year=1957, icon='https://upload.wikimedia.org/wikipedia/en/a/aa/BrilliantCornersTheloniousMonk.jpg', description="Cras in erat nulla. Donec vestibulum gravida leo, eget ultrices sapien maximus non. Duis varius vitae massa vitae varius. Phasellus ornare risus ac maximus ullamcorper. Nulla congue lacus vitae est faucibus iaculis ac a ex. Mauris id suscipit lacus. Aliquam neque tortor, cursus ut vehicula a, porttitor cursus nibh. Sed et nunc quam. Ut dignissim, mi ac ultricies mattis, arcu purus blandit enim, non iaculis erat sapien sed tellus. Nulla facilisi. Pellentesque non tempus lectus. Duis molestie sapien in leo fermentum, lobortis eleifend felis pharetra. Donec vel mollis ex, ac congue sem.", category_id=firstCat.id, user_id=firstUser.id)
session.add(item5)
session.commit()

item6 = Item(name='Thelonious Monk with John Coltrane', year=1957, icon='https://upload.wikimedia.org/wikipedia/en/6/62/TheloniousMonkWithJohnColtraneCover.jpg', description="In nec dictum odio, sit amet rutrum justo. Cras eget gravida dolor, vitae facilisis elit. Nullam nec consectetur quam, et rutrum nibh. Proin sed dapibus elit. Integer ultrices, augue in faucibus consectetur, neque felis iaculis sapien, vel scelerisque dui neque eget arcu. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras quam eros, rhoncus finibus lacus ac, sollicitudin egestas lectus. Cras vitae tristique massa. Curabitur at nibh ultricies, fermentum eros vitae, venenatis arcu. Nunc sodales interdum dui sit amet rhoncus. Integer tempor et eros ac tempor.", category_id=firstCat.id, user_id=firstUser.id)
session.add(item6)
session.commit()

item7 = Item(name="Monk's Dream", year=1963, icon='https://upload.wikimedia.org/wikipedia/en/e/ed/Monks_Dream_by_Thelonious.jpg', description="Aliquam erat volutpat. In blandit dolor at aliquam pulvinar. Donec interdum diam nulla, eget iaculis eros efficitur id. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nam ornare, justo eget hendrerit interdum, libero turpis elementum odio, vitae tincidunt purus lorem nec libero. Phasellus in erat vestibulum, ullamcorper purus eu, elementum urna. Vestibulum vel lectus molestie erat congue lobortis sed a nulla. Ut luctus et sem vitae dictum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi fermentum libero ut lacinia fringilla. Praesent tellus arcu, sodales vitae erat quis, placerat tincidunt tellus.", category_id=firstCat.id, user_id=firstUser.id)
session.add(item7)
session.commit()

secondCat = Category(name = "Brian Eno", user_id=firstUser.id)
session.add(secondCat)
session.commit()

item2 = Item(name='Here Come the Warm Jets', year=1974, icon='https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Warmjetsvinyl.jpg/220px-Warmjetsvinyl.jpg', description="In convallis ex ut nunc fringilla dapibus. Fusce vel tortor dapibus lorem auctor semper. Nulla eu risus eu neque facilisis sodales. Aliquam auctor elit eget diam aliquet rutrum. Morbi efficitur, leo et sagittis aliquam, risus mi ultrices dui, ut sagittis orci massa a lectus. In efficitur sodales justo eget aliquam. Donec a laoreet metus, eget porta sapien. Vestibulum in laoreet purus, at iaculis ligula. Sed in ipsum imperdiet, bibendum erat nec, convallis lacus. Quisque pellentesque at magna eget blandit. Aenean aliquet posuere maximus. Nam sollicitudin enim et dui fermentum, ut porta lacus volutpat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Praesent velit tellus, rutrum id sollicitudin eu, ultrices eget eros.", category_id=secondCat.id, user_id=firstUser.id)
session.add(item2)
session.commit()

item3 = Item(name='Taking Tiger Mountain (By Strategy)', year=1974, icon='https://upload.wikimedia.org/wikipedia/en/thumb/7/70/Tigermountaineno.jpg/220px-Tigermountaineno.jpg', description="Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas tempor feugiat turpis ac pulvinar. Fusce et nibh nunc. Integer aliquam eleifend felis eu elementum. Proin eu tellus faucibus sem interdum dignissim vel sed tellus. Morbi vulputate egestas ipsum, et fringilla nunc hendrerit sed. Cras facilisis ipsum pulvinar sollicitudin dapibus. Mauris euismod consectetur eros, a vehicula lacus rhoncus eget. Praesent sed ullamcorper nisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ut lorem interdum, fermentum ligula ut, dapibus purus. Integer in ligula ultrices, placerat sem nec, ornare dui.", category_id=secondCat.id, user_id=firstUser.id)
session.add(item3)
session.commit()

item4 = Item(name='Music For Airports', year=1978, icon='https://upload.wikimedia.org/wikipedia/en/thumb/4/46/Music_for_Airports.jpg/220px-Music_for_Airports.jpg', description="Nunc vel tristique nisi. Nullam feugiat lorem nec metus blandit venenatis vitae quis ante. Aliquam fermentum diam lectus, in consequat turpis sodales porttitor. Aliquam posuere neque faucibus sollicitudin maximus. Etiam elementum sagittis dapibus. Quisque pretium suscipit justo. Donec congue diam nibh, pulvinar mollis lectus mattis ac.", category_id=secondCat.id, user_id=firstUser.id)
session.add(item4)

session.commit()
