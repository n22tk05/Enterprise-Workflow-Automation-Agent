import { HttpService } from "@nestjs/axios";
import { Injectable, Logger } from "@nestjs/common";
import { AxiosError } from "axios";
import { catchError, firstValueFrom, pipe } from "rxjs";

@Injectable()
export class AiService {
  private readonly logger = new Logger(AiService.name);

  constructor(private readonly httpService: HttpService) {}

  async connectAi() {
    const data = await firstValueFrom(
      this.httpService.get("http://127.0.0.1:8000/connect").pipe(
        catchError((error: AxiosError) => {
          this.logger.error(error.response?.data || error.message);
          throw new Error("An error happened!");
        }),
      ),
    );

    return data.data;
  }

  async askAi(message: string, threadId: string) {
    console.log(message)
    const data = await firstValueFrom(
      this.httpService
        .post("http://127.0.0.1:8000/chat", {
          message,
          thread_id: threadId,
        })
        .pipe(
          catchError((error: AxiosError) => {
            this.logger.error(error.response?.data || error.message);
            throw new Error("An error happened!");
          }),
        ),
    );

    return data.data;
  }
}
