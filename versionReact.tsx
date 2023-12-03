import axios, { AxiosError } from "axios";
import { useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form"

type FormInputs = {
    artist: string,
    email: string,
}

export const Home = () => {

    const { register, handleSubmit, formState: { errors } } = useForm<FormInputs>()
    const MAX_RETRIES = 3;
    const RETRY_DELAY = 1000; // milliseconds
    type RequestResponseItem = {
        id: number;
        title: string;
        location : string;
        date : string;
        ticketUrl : string;
        pictureUrl : string; 
    }
    const arrayResponseList : RequestResponseItem[] = [];
    const [apiResponse, setApiResponse] = useState<RequestResponseItem[]>([]);
    const [selectedItem, setSelectedItem] = useState<RequestResponseItem | null>(null);
    const [connectionStatus, setConnectionStatus] = useState<string>('Non connecté');
    const [queryResult, setQueryResult] = useState<string>('');
    const [email, setEmail] = useState('');
    const [emailRequired, setEmailRequired] = useState('');
    var previousurl = '';

    const onSubmit : SubmitHandler<FormInputs> = data => {
        getInfo(data.artist, 0);
    }

    const getInfo = async (artist : FormInputs|string, retryCount = 0) => {
        const url = `https://www.seetickets.com/fr/search?q=${artist}`;
        try {
            const response = await axios.get(url);
            const htmlContent = response.data;

            //const articles = htmlContent.match(/<article class="result-text">(.*?)<\/article>/gs);
            const articles = htmlContent.match(/<a class="g-blocklist-link"(.*?)<\/a>/gs);
            console.log("Test en cours");
            if (articles) {
                console.log(articles.length);
                var i = 1;
                articles.forEach((article: any) => {
                // Process each article
                //console.log(article);
                const urlRegex = /<a.*?href="([^"]+)"/;
                const imageRegex = /<img[^>]+data-src="([^"]+)"/;
                const titleRegex = /<span class="event-title">([^<]+)<\/span>/;
                const locationRegex = /<br>([^<]+)<br>/;
                const dateRegex = /<time datetime="([^"]+)">([^<]+)<\/time>/g;

                const urlMatch = article.match(urlRegex);
                const imageMatch = article.match(imageRegex);
                const titleMatch = article.match(titleRegex);
                const locationMatch = article.match(locationRegex);
                const dateMatches = Array.from(article.matchAll(dateRegex));
                var date = '';
                //if we can't get the date, then we don't display the concert
                if(dateMatches.length !== 0)
                {
                    const dateMatch = dateMatches[1];
                    date = dateMatch as string;
                    if(date[1].length === 10)//Only display the concert if date if format "DD MM YYYY"
                    {
                        const concertUrl = "https://www.seetickets.com" + urlMatch ? "https://www.seetickets.com" + urlMatch[1] : '';
                        const imageUrl = (imageMatch ? imageMatch[1] : '').replace("https://statics.digitick.com/commun/images/upload/events/f7/1c/defaut_110.png", "https://www.alsace.catholique.fr/wp-content/uploads/sites/14/2015/11/sablier.png");
                        const title = (titleMatch ? titleMatch[1] : '').replaceAll("&#xE9;", "é").replaceAll("&#x27;", " ").replaceAll("&#x2B;", "+").replaceAll("&#xFC;", "ü").replaceAll("&#xF4;", "ô").replaceAll("&#xEA;", "ê").replaceAll("&#xE8;","è");
                        const location = (locationMatch ? locationMatch[1].trim() : '').replaceAll("&#xE9;", "é").replaceAll("&#x27;", " ").replaceAll("&#x2B;", "+").replaceAll("&#xFC;", "ü").replaceAll("&#xF4;", "ê").replaceAll("&#xE8;","è");
                        //console.log("url: "+ concertUrl);
                        //console.log("image: "+imageUrl);
                        //console.log("artist: "+title);
                        //console.log("emplacement: "+location);
                        //console.log("date: "+ date[1]);
        
                        const arrayResponse : RequestResponseItem = 
                        {
                            id: i,
                            title: title,
                            location : location,
                            date : date[1],
                            ticketUrl : concertUrl,
                            pictureUrl : imageUrl,
                        }
                        arrayResponseList.push(arrayResponse);
                        i++;
                    }
                }
                else{
                    setQueryResult("Cet artiste n'a pas de concerts en ce moment !");
                    console.log("Cet artiste n'a pas de concert en ce moment");
                }
            });
            setApiResponse(arrayResponseList);
            }
          } catch (error) {
            if (retryCount < MAX_RETRIES) {
              // Retry after a delay
              await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
              getInfo(artist, retryCount + 1);
            } else {
              // Handle maximum retries exceeded
              console.error('Failed to fetch data:', (error as AxiosError).message);
            }
          }
    }

    const saveDataToDatabase = async (dataToSave : RequestResponseItem | null) => {
        if(isValidEmail()){
            axios.post('http://localhost:3001/api/insert', {
                artist: dataToSave?.title,
                location: dataToSave?.location,
                email: email,
                url: dataToSave?.ticketUrl,
                end_date: dataToSave?.date
            })
            setEmailRequired("Vous serez informé par email dès la sortie de nouvelles places !");
        }
        else{
            setEmailRequired('Une adresse email est attendue');
        }
    }

    const handleInputChange = (event: { target: { value: any; }; }) => {
        setEmail(event.target.value);
    };

    const isValidEmail = () => {
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailRegex.test(email);
    }

    const selection = (item : RequestResponseItem) => {
        if(item.ticketUrl !== previousurl)
        {
            setSelectedItem(item);
            setEmail('');
            previousurl = item.ticketUrl;
        }
        else{
            setSelectedItem(item);
            setEmailRequired('');
        }
    }

    return (
        <main>
            <center>
                <div className="mt-20">
                    <h1 className="font-extrabold mb-4 text-3xl">notiftonconcert</h1>
                    <p>Reçois une notif par mail dès que des places pour ton prochain concert sont de nouveau disponibles</p>
                    
                    <form  onSubmit={handleSubmit(onSubmit)}>
                        <div className="container-form">
                            <label className="block mb-1" htmlFor="artist">Entrer le concert à voir ici</label>
                            <input {...register("artist", {required: true})} className="border mr-2 w-full px-2" type='text' name="artist" id="artist" placeholder="Par exemple: Orelsan, Angèle..."/>
                            {errors.artist && <p className="text-[red]  mb-5">Nom d'artiste attendu</p>}
                            {queryResult !== "" && <p className="text-[red]  mb-5">{queryResult}</p>}
                        </div>
                        

                        <input type='submit' value="OK" className="block bg-[purple] text-[white] py-3 px-3 hover:bg[red]"/>
                    </form>

                    <ul className="concert-list">
                        {apiResponse.map((item) => (
                            <li
                                key={item.id}
                                className={`concert-item ${selectedItem === item ? 'selected' : ''}`}
                                onClick={() => selection(item)}
                            >
                            <img src={item.pictureUrl} alt={item.title} className="concert-image" />
                            <div className="concert-info">
                            <h2>{item.title}</h2>
                            <p>Emplacement: {item.location}</p>
                            <p>Date: {item.date}</p>
                            {selectedItem === item && (
                                <><input type="text" value={email} onChange={handleInputChange} placeholder="Entre ton adresse email"/>
                                <button onClick={() => saveDataToDatabase(item)}>M'informer des nouvelles dispo</button>
                                {emailRequired !== "Vous serez informé par email dès la sortie de nouvelles places !" && <p className="text-[red]  mb-5">{emailRequired}</p>}
                                {emailRequired === "Vous serez informé par email dès la sortie de nouvelles places !" && <p className="text-[green]  mb-5">{emailRequired}</p>}</>
                              )}
                            </div>
                        </li>
                        ))}
                    </ul>
                </div>
            </center>
        </main>
        
    )
}
