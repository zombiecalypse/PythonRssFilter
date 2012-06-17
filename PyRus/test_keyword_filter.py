# vim: set fileencoding=utf8 :
from testtools import TestCase
from testtools.matchers import *
from testtools.testcase import ExpectedException
from ludibrio import Stub

from .test_helpers import *

from .filters import *
import nltk

reddit_string = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
  <channel>
    <title>Poetry</title>
    <link>http://www.reddit.com/r/Poetry/</link>
    <description></description>
    <item>
      <title>Snakes</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/</link>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/</guid>
      <pubDate>Thu, 26 Apr 2012 02:27:01 -0700</pubDate>
      <description>this is a text with a python.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gset5</guid>
      <title>farsightedness on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gset5</link>
      <dc:date>2012-04-26T02:27:19.417150-07:00</dc:date>
      <description>[The Charge of the Light Brigade](http://www.ram.org/contrib/the_charge_of_the_light_brigade.html) by Alfred Lloyd Tennyson is a poem about a failed British cavalry charge in an obscure war (cavalry = soldiers on horseback). The cavalry brigade was given a suicidal order by accident: to charge straight through the Russian cannon line. When they read the order they knew it was certain death, but they carried it out anyway. This poem is awesome because it is a masterful demonstration of the use of meter (rhythm) to add to meaning. When you read it, you should read it out loud so that you hear the rhythm. Take a look at the first four lines: &amp;quot;Half a league, half a league, Half a league onward, All in the valley of Death Rode the six hundred.&amp;quot; How would you describe the sound of the language? Tennyson alternates between hard and soft syllables, creating a cool rhythmic effect that sounds like the galloping of cavalry horses: &amp;quot;**Half** a **league**, **Half** a **league**, &amp;quot;**Half** a **league** **on**ward&amp;quot;, Imagine instead if he had written it this way: &amp;quot;A half league, a half league, A half league onward&amp;quot; Instead of galloping, the horses sound like they are dying from exhaustion! We can see that Tennyson made the correct decision. All throughout the poem, Tennyson strictly keeps to only 4 different rhythm patterns for all his lines. 1) &amp;quot;**Half** a **league**, **half** a **league**&amp;quot; 2) &amp;quot;**Rode** the **six** **hun**dred&amp;quot; 3) &amp;quot;**All** in the **val**ley of **Death**&amp;quot; 4) &amp;quot;**Back** from the **mouth** of **hell**&amp;quot; Keeping to strict form causes the variations to stick out and have their own personality. If he had written each line haphazardly in an arbitrary rhythm, they would lose their distinctiveness. Notice that one pattern ends on an unstressed syllable - &amp;quot;**Half** a **league** **on**ward&amp;quot;. These lines have an unfinished feel that give the poem momentum. The ear desires a hard ending, and goes looking to the next line for it. Soft (&amp;quot;feminine&amp;quot;) endings are a great way to point a reader to the next line, to develop tension and then give resolution. If you're interested in learning more about meter, I encourage you to check out [this detailed blog post](http://strongverse.blogspot.com/2008/03/basic-english-prosody.html) by r/poetry's own gmpalmer.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h2knd</guid>
      <title>saintboniface on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h2knd</link>
      <dc:date>2012-04-26T17:54:51.715812-07:00</dc:date>
      <description>[Here](http://www.youtube.com/watch?v=MkqUq26z1CE) is a recording of Tennyson reading the poem. If you can ignore the creepy animation, it's a great way to hear the poem in the way that Tennyson intended it to be heard. **edit** It helps to have the poem to read along with the recording, as it's a cylinder recording and not very clear.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h762y</guid>
      <title>farsightedness on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h762y</link>
      <dc:date>2012-04-27T01:04:12.699277-07:00</dc:date>
      <description>Also see http://www.youtube.com/watch?v=Qke-zjjYssM</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gtak9</guid>
      <title>TomCook24 on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gtak9</link>
      <dc:date>2012-04-26T05:25:54.717819-07:00</dc:date>
      <description>[Drummer Hodge](http://www.poemhunter.com/poem/drummer-hodge/) is a poem by Thomas Hardy about an anonymous drummer boy, probably in the Boer war, who has fallen in battle. The name 'Hodge' was their equivalent of 'John Doe' at the time. The poem is a ballad, and one of the most perfect examples I can think of. It has the charming balance of emotive content and excellent poetic technique. It also reminds me somewhat of Rupert Brooke, and his allusion that there is some corner of a foreign field that is forever England. Fairly self explanatory in both content and style, it is a riveting example of poetry at its best.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gxpnk</guid>
      <title>farsightedness on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gxpnk</link>
      <dc:date>2012-04-26T11:41:14.203614-07:00</dc:date>
      <description>The last paragraph is quite spooky: &amp;quot;His homely Northern breast and brain Grow to some Southern tree,&amp;quot; I like, I like.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gwc0p</guid>
      <title>garyp714 on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gwc0p</link>
      <dc:date>2012-04-26T09:57:31.846865-07:00</dc:date>
      <description>Fellow poets: please upvote this so all users can check out this as it will be a reoccurring thing. Self posts = no karma! Thanks</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gx6o1</guid>
      <title>farsightedness on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gx6o1</link>
      <dc:date>2012-04-26T11:02:17.542160-07:00</dc:date>
      <description>Also, check out this [awesome comment](http://www.reddit.com/r/Poetry/comments/ss3n4/bygones/c4gt8er) by madducks explaining his concrete poem, &amp;quot;bygones&amp;quot;</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h1m9m</guid>
      <title>BeepBopBoop123 on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h1m9m</link>
      <dc:date>2012-04-26T16:38:03.885282-07:00</dc:date>
      <description>Ode To an Atom By Pablo Neruda Infinitesimal star, you seemed forever buried in metal, hidden, your diabolic fire. One day someone knocked at your tiny door: it was man. With one explosion he unchained you, you saw the world, you came out into the daylight, you traveled through cities, your great brilliance illuminated lives, you were a terrible fruit of electric beauty, you came to hasten the flames of summer, and then wearing a predator's eyeglasses, armor, and a checked shirt, sporting sulfuric mustaches and a prehensile tail, came the warrior and seduced you: sleep, he told you, curl up, atom, you resemble a Greek god, a Parisian modiste in springtime, lie down here on my fingernail, climb into this little box and then the warrior put you in his jacket as if you were nothing but a North American pill, and he traveled through the world and dropped you on Hiroshima. We awakened. The dawn had been consumed. All the birds burned to ashes. An odor of coffins, gas from tombs, thundered through space. The shape of punishment arose, hideous, superhuman, bloody mushroom, dome, cloud of smoke, sword of hell. Burning air arose, speeding death on parallel waves, reaching the mother sleeping with her child, the river fisherman and the fish, the bakery and the bread, the engineer and his buildings; everything was acid dust, assassin air. The city crumbled its last honeycombs and fell, fell suddenly, demolished, rotten; men were instant lepers, they took their children's hand and the little hand fell off in theirs. So, from your refuge in the secret mantle of stone in which fire slept they took you, blinding spark, raging light, to destroy lives, to threaten distant existences, beneath the sea, in the air, on the sands, in every twist and turn of the ports, to destroy seeds, to kill cells, to stunt the corolla, they destined you, atom, to level nations, to turn love into a black pustule to burn heaped-up hearts and annihilate blood. Mad spark, go back to your shround, bury yourself in your mineral mantle, be blind stone once again, ignore the outlaws, and collaborate with life, with growing things, replace motors, elevate energy, fertilize planets. You have no secret now, walk among men without your terrible mask, pick up your pace and pace the picking of the fruit, parting mountains, straightening rivers, making fertile, atom, overflowing cosmic cup, return to the peace of the vine, to the velocity of joy, return to the province of nature, place yourself at our service, and instead of the fatal ashes of your mask, instead of the unleashed infernos of your wrath, instead of the menace of your terrible light, deliver to us your amazing rebelliousness for your grain, your unchained magnetism to found peace among men, and then your dazzling light will be happiness, not hell, hope of morning, gift to earth. Pablo Neruda is classical seen as the master of Ode. an Ode, in its most pure of forms, seeks to love the thing that it represents, in this case the Atom. This is much easier said than done. One can love their mother, they can love their spouse, their crush, they can even love the one that they hate. These are fathomable candidates for one's love. But only a truly insane person can love an object with not living thinking animations of its own, and especially one that you can only conceptually know about, and not see. Neruda proves that he can love an atom and gives it as many and more animations as a living creature can possibly having, making the impetus to love the Atom all that much more. But the poem is also not without its point. It's love of the atom is also an indictment of mankind for misusing a basic property of living, and a wonderful one at that. He displays the splendor of the atom's origins (a star) and seeks to have the atom be apart of the life giving world instead of being swayed by man for man's destructive desires. The gentle descriptions seem to be something that is lost on poets these days. The highly selected words are so profound in their economy that Neruda is forced to place important ones on a line of their own. The characterizations and the narratives that spring from these lines are the wit and soul of poetry - as an ode inevitably doubles as an ode to itself, to poetry.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h2czn</guid>
      <title>saintboniface on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h2czn</link>
      <dc:date>2012-04-26T17:38:07.423735-07:00</dc:date>
      <description>Ars Poetica (cocoons) by Dana Levin Six monarch butterfly
      cocoons clinging to the back of your throat— you could feel their gold
      wings trembling. You were alarmed. You felt infested. In the downstairs
      bathroom of the family home, gagging to spit them out— and a voice saying
      Don’t, don’t— An ars poetica is a poem about writing poetry or the art of
      poetry. What makes ars poeticas so difficult for many poets to write is
      trying to express the writing process in a way that is both unique and
      able to be understood by readers (poets and non-poets alike). Like love
      poetry, it's very difficult to write an ars poetica without reverting to
      cliched images, mainly because it's one of the oldest forms of poetry.
      Dana Levin is able to write about poetry without actually mentioning
      poetry, except in the title. This is an excellent example of why titles
      are an essential part of a poem. Without being guided to read this as an
      ars poetica at the beginning, the reader would not be able to understand
      the cocoons/butterflies as a metaphor for poetic inspiration. Another
      great thing about this poem is the central image. Levin incorporates a
      common image in poetry (butterflies), but uses it in a way that is fresh
      and surprising. Instead of being a metaphor for beauty and freedom, their
      presence is parasitic and traumatizing to the subject. The speaker is a
      vessel, not a voluntary host. This image conveys the idea of writing as a
      involuntary, sometimes emotionally exhausting act. This is an idea that
      has been expressed by many writers. Levin expresses this clearly, but in a
      way that also seems personal. The use of the second person helps make the
      poem seem communal by the speaker addressing the plural
      &amp;quot;you&amp;quot; of the audience. Pretty impressive for only three
      stanzas!</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h75rl</guid>
      <title>farsightedness on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h75rl</link>
      <dc:date>2012-04-27T01:02:37.367316-07:00</dc:date>
      <description>Ooo, you taught me a new term. This is a lovely poem, too!</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h4fti</guid>
      <title>hyper_thymic on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h4fti</link>
      <dc:date>2012-04-26T20:15:26.406576-07:00</dc:date>
      <description>The Flea -John Donne Mark but this flea, and mark in this, How little that which thou deniest me is; It suck'd me first, and now sucks thee, And in this flea our two bloods mingled be. Thou know'st that this cannot be said A sin, nor shame, nor loss of maidenhead; Yet this enjoys before it woo, And pamper'd swells with one blood made of two; And this, alas! is more than we would do. O stay, three lives in one flea spare, Where we almost, yea, more than married are. This flea is you and I, and this Our marriage bed, and marriage temple is. Though parents grudge, and you, we're met, And cloister'd in these living walls of jet. Though use make you apt to kill me, Let not to that self-murder added be, And sacrilege, three sins in killing three. Cruel and sudden, hast thou since Purpled thy nail in blood of innocence? Wherein could this flea guilty be, Except in that drop which it suck'd from thee? Yet thou triumph'st, and say'st that thou Find'st not thyself nor me the weaker now. 'Tis true; then learn how false fears be; Just so much honour, when thou yield'st to me, Will waste, as this flea's death took life from thee. The conceit is a device a poet uses to take a metaphor and extend it for the length of the poem and to a logical extreme. In this case, Donne asks his mistress, &amp;quot;If we've already mixed bodily fluids in the flea, why not do it sexually?&amp;quot; The image of the flea works on many levels: it is the mingler of their blood, the temple of their &amp;quot;marriage,&amp;quot; and, finally, when the mistress pinches it to death between her thumb and forefinger, a symbol both of the death of Donne's desire and of the hollowness of the mistress's honor. Conceits are often the engines that drive structured poems such as sonnets, but it could also be argued that modern poems such as Williams' The Red Wheelbarrow or St. Vincent Millay's &amp;quot;My candle burns at both ends&amp;quot; are also employing conceits.</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gwtql</guid>
      <title>madducks on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4gwtql</link>
      <dc:date>2012-04-26T10:34:49.686650-07:00</dc:date>
      <description>[The Prose Poem](http://www.poets.org/viewmedia.php/prmMID/16561) by Campbell McGrath is a beautiful, instructive poem. It teaches not just about prose poetry, but extended metaphor, sonics, and imagery. Every image informs the subject matter, and somehow never explicitly. Sacrificing line breaks McGrath shows meticulously how every poetic device still operates at an effective level. For instance, while talking about the place of formalism in prose poetry, maybe even contemporary poetry in general, he reinforces his point by falling into meter: &amp;gt; **here** and **there** a **wea**thered **post** a**sserts** a **for**mer **claim** The rich landscape is accompanied by just as rich language and sound. The nouns are strong and vivid: *map, chessboard, margin, swale, rill, rivulet, gully, dell, bracken, strands* The adjectives are so apt that they almost don't need anchoring to their nouns. It's hard to talk about how much I admire this poem without ending up quoting the entire thing... Close rereading of this poem is rewarded, and the poem doesn't seal itself off, it ends, acrobatically with what at first glance seems like a rhetoric question but ends inviting you back into the poem, over and over again to thresh its fields for more meaning yet: &amp;gt;You've passed this way yourself many times, and can tell me, if you would, do the formal fields end where the valley begins, or does everything that surrounds us emerge from its embrace?</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h14kn</guid>
      <title>kolembo on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4h14kn</link>
      <dc:date>2012-04-26T15:57:10.433113-07:00</dc:date>
      <description>Two great poems I came across from Hans-magnus Enzensberger , translated from the German by Peter Lachnewinsky http://peterlachnewinsky.wordpress.com/2011/01/15/hans-magnus-enzensberger-two-early-poems/#comment-1149 Gorgeous because I was astonished how image translates so easily, moved because of how apparant wider politics affects lives</description>
    </item>
    <item>
      <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4laa1h</guid>
      <title>XXJX on Learning Thursday: Share a poetry technique with your fellow redditors</title>
      <link>http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/c4laa1h</link>
      <dc:date>2012-05-07T15:48:14.630496-07:00</dc:date>
      <description>After Auschwitz by Anne Sexton Anger, as black as a hook, overtakes me. Each day, each Nazi took, at 8: 00 A.M., a baby and sauteed him for breakfast in his frying pan. And death looks on with a casual eye and picks at the dirt under his fingernail. Man is evil, I say aloud. Man is a flower that should be burnt, I say aloud. Man is a bird full of mud, I say aloud. And death looks on with a casual eye and scratches his anus. Man with his small pink toes, with his miraculous fingers is not a temple but an outhouse, I say aloud. Let man never again raise his teacup. Let man never again write a book. Let man never again put on his shoe. Let man never again raise his eyes, on a soft July night. Never. Never. Never. Never. Never. I say those things aloud. I beg the Lord not to hear. Anne Sexton has long been a favorite poet of mine. Her poetry is very raw and interesting. One the things that make her such a great poet is her ability to create specific (sometimes grotesque) images that accurately portray the meaning in her poems. A friend of mine described images like this: Imagine your poem as a water tower, your point is the water inside of the tower. However, poetry is something that is manageable, but moving. With manageability in mind, a water tower can be related to a broad idea. So, instead of your poem being a water tower, compress all of the water in the large tower, and press it into a bottle of water. Basically, make your images and poems something that portrays your point, but in a quick and gripping manner.</description>
    </item>
  </channel>
</rss>"""
xkcd_string = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
xml:lang="en"><title>xkcd.com</title><link href="http://xkcd.com/"
rel="alternate"></link><id>http://xkcd.com/</id><updated>2012-06-01T00:00:00Z</updated><entry><title>Kill
Hitler</title><link href="http://xkcd.com/1063/"
rel="alternate"></link><updated>2012-06-01T00:00:00Z</updated><id>http://xkcd.com/1063/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/kill_hitler.png"
title="Revised directive: It is forbidden for you to interfere with human
history until you've at least taken a class on it." alt="Revised directive: It
is forbidden for you to interfere with human history until you've at least taken
a class on it." /&gt;</summary></entry><entry><title>Budget News</title><link
href="http://xkcd.com/1062/"
rel="alternate"></link><updated>2012-05-30T00:00:00Z</updated><id>http://xkcd.com/1062/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/budget_news.png" title="I
will vote, no questions asked, for any candidate who describes themselves as
'more of a deficit sugar glider.'" alt="I will vote, no questions asked, for any
candidate who describes themselves as 'more of a deficit sugar glider.'"
/&gt;</summary></entry><entry><title>Snake</title><link
href="http://xkcd.com/1061/"
rel="alternate"></link><updated>2012-05-28T00:00:00Z</updated><id>http://xkcd.com/1061/</id><summary
type="html">There is a
huge python there.</summary></entry><entry><title>Crowdsourcing</title><link
href="http://xkcd.com/1060/"
rel="alternate"></link><updated>2012-05-25T00:00:00Z</updated><id>http://xkcd.com/1060/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/crowdsourcing.png"
title="We don't sell products; we sell the marketplace. And by 'sell the
marketplace' we mean 'play shooters, sometimes for upwards of 20 hours
straight.'" alt="We don't sell products; we sell the marketplace. And by 'sell
the marketplace' we mean 'play shooters, sometimes for upwards of 20 hours
straight.'" /&gt;</summary></entry></feed>"""











class KeywordFilterTest(TestCase):
    @Test
    def keyword_filter(self):
        self.filter = KeywordFilter('python')
        self.pipe = (GetFeed(reddit_string) & GetFeed(xkcd_string)) >> self.filter >> DictSink('xkcd and reddit')
        self.result = self.pipe(None)

    @Test
    def strict_keyword_filter(self):
        self.filter = KeywordFilter('python', 'huge')
        self.pipe = (GetFeed(reddit_string) & GetFeed(xkcd_string)) >> self.filter >> DictSink('xkcd and reddit')
        self.result = self.pipe(None)


    @Given(keyword_filter)
    def keeps_interesting_stuff(self):
        self.assertThat(self.result, IsInstance(dict))
        self.assertThat(self.result, Contains('entries'))
        self.assertThat([e['title'] for e in self.result['entries']],
                MatchesSetwise(
                    Equals('[xkcd.com] Snake'), 
                    Equals('[Poetry] Snakes')))

    @Given(strict_keyword_filter)
    def keeps_interesting_stuff_adding_filters(self):
        self.assertThat(self.result, IsInstance(dict))
        self.assertThat(self.result, Contains('entries'))
        self.assertThat([e['title'] for e in self.result['entries']],
                MatchesSetwise(
                    Equals('[xkcd.com] Snake')))
